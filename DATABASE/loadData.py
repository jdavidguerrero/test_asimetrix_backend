import pandas as pd
from sqlalchemy import create_engine
import psycopg2

engine = create_engine("postgresql+psycopg2://tsdbadmin:dm4mztd0jv0uvjla@plo7lhif44.h6oblrgc5x.tsdb.cloud.timescale.com:35696/tsdb")


df = pd.read_excel ('output.xlsx', sheet_name='Sheet1', header=0)
print (df)
df.to_sql(name='data', con=engine, if_exists='append', index=False)