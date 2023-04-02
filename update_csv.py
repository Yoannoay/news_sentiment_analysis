from sqlalchemy import create_engine
import pandas as pd
import spacy 
import numpy as np 
import psycopg2
import os 

user = os.environ.get('postgres_user')
password = os.environ.get('postgres_pass')

def create_table():
        conn = psycopg2.connect(host='localhost', database='world_news_analysis',
                                user=user, password =password)
        cur = conn.cursor()

        sky_table = "SELECT * FROM sky_news"
        cbs_table = "SELECT * FROM cbs_news"
        dw_table = "SELECT * FROM dw_news"
        lemonde_table = "SELECT * FROM lemonde_news"

        sky_df = pd.read_sql(sky_table, conn)
        cbs_df = pd.read_sql(cbs_table, conn)
        dw_df = pd.read_sql(dw_table, conn)
        lemonde_df = pd.read_sql(lemonde_table, conn)
        
        
        conn.close()

        df = pd.concat([sky_df, cbs_df, dw_df, lemonde_df], ignore_index=True)
        csv = f"C:\\Users\\yoanc\\Documents\\World_News_Analysis_v.1\\Streamlit\\Complete_news_data.csv"

        if os.path.exists(csv):
                os.remove(csv)
        df.to_csv(csv)
        

create_table()