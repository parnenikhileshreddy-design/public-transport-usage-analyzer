import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'data' / 'processed' / 'sample_transport_data.csv'
rng = np.random.default_rng(42)

cities = ['London','New York','Berlin','Tokyo','Paris','Singapore']
city_factor = {'London':1.0,'New York':1.15,'Berlin':0.82,'Tokyo':1.35,'Paris':1.05,'Singapore':0.92}
modes = ['bus','metro','rail','tram','lrt']
rows=[]
start = pd.Timestamp('2026-01-01')
dates = pd.date_range(start, periods=120, freq='D')
for city in cities:
    for route_num in range(1, 9):
        route = f'{city[:3].upper()}-{route_num:02d}'
        mode = modes[(route_num-1) % len(modes)]
        base = (70 + route_num*12) * city_factor[city] * (1.15 if mode=='metro' else 1.0)
        for d in dates:
            dow = d.dayofweek
            for hour in range(6, 23):
                peak = 1.75 if hour in (8,9,17,18,19) else (1.25 if hour in (7,10,16,20) else 0.72)
                weekend = 0.72 if dow >= 5 else 1.0
                trend = 1 + 0.0015*(d-start).days
                noise = rng.normal(1.0, 0.12)
                passengers = max(5, int(round(base*peak*weekend*trend*noise)))
                capacity = 120 if mode in ('bus','tram','lrt') else 220
                occupancy = min(1.25, passengers/capacity + rng.normal(0,0.03))
                delay = max(0, int(round(rng.gamma(2.0, 1.2) + (3 if occupancy>0.9 else 0))))
                rows.append([d.date(),city,route,mode,hour,dow,passengers,capacity,occupancy,delay])

df = pd.DataFrame(rows, columns=['date','city','route','mode','hour','day_of_week','passengers','capacity','occupancy_rate','delay_minutes'])
df['utilization'] = np.where(df.passengers/df.capacity >= .85,'High',np.where(df.passengers/df.capacity >= .55,'Medium','Low'))
df['peak_period'] = df.hour.isin([8,9,17,18,19]).map({True:'Peak',False:'Off-Peak'})
OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT,index=False)
print(f'Wrote {len(df):,} rows to {OUT}')
