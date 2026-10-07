from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'processed'/'sample_transport_data.csv'
OUT=ROOT/'outputs'

def load():
    df=pd.read_csv(DATA, parse_dates=['date'])
    if (df['passengers']<0).any(): raise ValueError('Invalid negative passenger count')
    df['date']=pd.to_datetime(df['date'])
    return df

def main():
    df=load(); OUT.mkdir(exist_ok=True)
    route=(df.groupby(['route','city','mode'],as_index=False)['passengers'].sum().sort_values('passengers',ascending=False))
    route.to_csv(OUT/'route_summary.csv',index=False)
    hourly=df.groupby('hour',as_index=False)['passengers'].mean().sort_values('passengers',ascending=False)
    hourly.to_csv(OUT/'hourly_summary.csv',index=False)
    city=df.groupby('city',as_index=False).agg(total_passengers=('passengers','sum'),avg_passengers=('passengers','mean'),avg_occupancy=('occupancy_rate','mean'),avg_delay=('delay_minutes','mean')).sort_values('total_passengers',ascending=False)
    city.to_csv(OUT/'city_summary.csv',index=False)
    peak=hourly.iloc[0]
    high=(df['utilization']=='High').mean()*100
    print('Rows:',len(df)); print('Peak hour:',int(peak.hour)); print('High utilization share: %.2f%%'%high); print('\nTop routes:\n',route.head(10).to_string(index=False))

if __name__=='__main__': main()
