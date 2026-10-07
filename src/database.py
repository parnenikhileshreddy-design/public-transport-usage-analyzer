import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT/'database'/'transport.db'
DATA = ROOT/'data'/'processed'/'sample_transport_data.csv'

def init_db():
    DB.parent.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    with sqlite3.connect(DB) as con:
        df.to_sql('transport_usage', con, if_exists='replace', index=False)
        con.execute('CREATE INDEX IF NOT EXISTS idx_route ON transport_usage(route)')
        con.execute('CREATE INDEX IF NOT EXISTS idx_date ON transport_usage(date)')
    return DB

def query(sql):
    with sqlite3.connect(DB) as con:
        return pd.read_sql_query(sql, con)

if __name__ == '__main__':
    print(init_db())
