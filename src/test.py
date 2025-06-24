import pandas as pd
import psycopg2
conn_params={
    "host": "postgres",        # or your server/container IP
    "port": "5432",
    "database": "test_db",
    "user": "user",
    "password": "root"

}

conn=psycopg2.connect(**conn_params)
query='select * from "public.stg_Shooting"'
df=pd.read_sql_query(query,conn)
conn.close()
df.to_csv('test.csv',index=False)

while True:
    pass