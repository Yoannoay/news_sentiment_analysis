import datetime 
import pandas as pd 
import time
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import spacy 
import numpy as np

import os 


def append_standard_topic(table_name):
        conn = psycopg2.connect(host='localhost', database='world_news',
                                user='postgres', password ='supremeoverlordYC7')
        engine = create_engine('postgresql://postgres:supremeoverlordYC7@localhost/world_news')

        cur = conn.cursor()
        #adding a column to take in the new values
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN standardised_topic TEXT;")


        #reading in the table to a dataframe to apply the new column values 
        df = pd.read_sql_table(table_name, engine)

        df['standardised_topic'] = df['topic'].apply(apply_closest_topic)

        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)


def apply_closest_topic(topic):
    
    # Load spaCy's English model
         nlp = spacy.load('en_core_web_lg')

        # Define your predefined list of topics
         topics = ['politics news', 'sports news', 'business and technology news', 'world news', 'domestic news', 'science news', 'health news', 'education news']

    
         if type(topic) == list:
                new_topic = []
                for t in topic:
                        doc = nlp(t)
                        sim = [doc.similarity(nlp(tt)) for tt in topics]
                        new_topic.append(topics[np.argmax(sim)])
                return new_topic
         else:
                doc = nlp(topic)
                sim = [doc.similarity(nlp(tt)) for tt in topics]
                return topics[np.argmax(sim)]
         

append_standard_topic("cbs_news")
append_standard_topic("sky_news")
append_standard_topic("dw_news")
append_standard_topic("lemonde_news")