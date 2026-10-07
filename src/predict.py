from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'processed'/'sample_transport_data.csv'
MODEL=ROOT/'outputs'/'demand_model.joblib'

def train():
    df=pd.read_csv(DATA,parse_dates=['date']).sort_values('date')
    df['day_of_month']=df.date.dt.day
    df['month']=df.date.dt.month
    features=['hour','day_of_week','day_of_month','month','capacity','occupancy_rate','delay_minutes']
    # Chronological split prevents future leakage.
    cut=int(len(df)*0.8)
    X_train,y_train=df.iloc[:cut][features],df.iloc[:cut].passengers
    X_test,y_test=df.iloc[cut:][features],df.iloc[cut:].passengers
    model=RandomForestRegressor(n_estimators=120,max_depth=14,random_state=42,n_jobs=-1)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    mae=mean_absolute_error(y_test,pred); r2=r2_score(y_test,pred)
    MODEL.parent.mkdir(exist_ok=True); joblib.dump((model,features),MODEL)
    print(f'MAE: {mae:.2f} passengers'); print(f'R2: {r2:.4f}'); print('Model:',MODEL)
    return mae,r2

if __name__=='__main__': train()
