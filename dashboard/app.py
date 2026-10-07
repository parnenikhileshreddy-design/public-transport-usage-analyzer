import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'processed'/'sample_transport_data.csv'
df=pd.read_csv(DATA,parse_dates=['date'])

st.set_page_config(page_title='Public Transport Usage Analyzer',page_icon='🚌',layout='wide')
st.title('🚌 Public Transport Usage Analyzer')
st.caption('Course End Project 9 • Batch-9 • 25881A05DG | 25881A05DH | 25881A05DJ')

with st.sidebar:
    st.header('Filters')
    city=st.multiselect('City',sorted(df.city.unique()),default=sorted(df.city.unique()))
    mode=st.multiselect('Mode',sorted(df["mode"].unique()),default=sorted(df["mode"].unique()))
    routes=st.multiselect('Route',sorted(df.route.unique()),default=[])

f=df[df.city.isin(city)&df["mode"].isin(mode)].copy()
if routes: f=f[f.route.isin(routes)]

c1,c2,c3,c4=st.columns(4)
c1.metric('Total passengers',f'{f.passengers.sum():,.0f}')
c2.metric('Avg / observation',f'{f.passengers.mean():,.1f}')
c3.metric('Peak hour',f"{int(f.groupby('hour').passengers.mean().idxmax()):02d}:00")
c4.metric('High utilization',f"{(f.utilization.eq('High').mean()*100):.1f}%")

left,right=st.columns(2)
with left:
    h=f.groupby('hour',as_index=False).passengers.mean()
    st.plotly_chart(px.line(h,x='hour',y='passengers',markers=True,title='Average Passenger Demand by Hour'),use_container_width=True)
with right:
    r=f.groupby('route',as_index=False).passengers.sum().sort_values('passengers',ascending=False).head(12)
    st.plotly_chart(px.bar(r,x='passengers',y='route',orientation='h',title='Top Routes by Passenger Volume'),use_container_width=True)

left,right=st.columns(2)
with left:
    d=f.groupby('date',as_index=False).passengers.sum()
    st.plotly_chart(px.line(d,x='date',y='passengers',title='Daily Passenger Trend'),use_container_width=True)
with right:
    u=f.groupby(['city','utilization'],as_index=False).size()
    st.plotly_chart(px.bar(u,x='city',y='size',color='utilization',barmode='group',title='Utilization by City'),use_container_width=True)

st.subheader('Route Summary')
summary=f.groupby(['route','city','mode'],as_index=False).agg(total_passengers=('passengers','sum'),avg_passengers=('passengers','mean'),avg_delay=('delay_minutes','mean'),avg_occupancy=('occupancy_rate','mean')).sort_values('total_passengers',ascending=False)
st.dataframe(summary,use_container_width=True,hide_index=True)

st.info('AI/ML extension: run src/predict.py to train the demand-forecasting model. The model uses a chronological 80/20 split to avoid future-data leakage.')
