import datetime 
import pandas as pd 
import time
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import spacy 
import numpy as np

import os 

#credentials
user = os.environ.get('postgres_user')
password = os.environ.get('postgres_pass')



class Logger:

    def __init__(self,news_source, suffix, csv):
       self.news_source = news_source
       self.suffix = suffix
       self.csv = csv
       self.df = pd.read_csv(csv)
       self.create_new_table()
       
       
       
    def create_new_table(self):
         engine = create_engine(f'postgresql://{user}:{password}@localhost/world_news_analysis')    
         name = str(self.news_source.lower())
         #creating table
         create_table = f"CREATE TABLE IF NOT EXISTS {name}(\
                    date DATE NOT NULL DEFAULT CURRENT_DATE,\
                    news_source TEXT NOT NULL,\
                    title TEXT NOT NULL,\
                    article TEXT NOT NULL,\
                    topic TEXT NULL,\
                    standardised_topic TEXT NOT NULL)"
    
         engine.execute(create_table)
    
         # making csv a dataframe so it can be used in the similiarity method
         df = pd.read_csv(self.csv)

         df['standardised_topic'] = df['topic'].apply(self.apply_closest_topic)

         df.to_sql(name=name, con=engine, if_exists='append', index=False)

        
    
    # Defining a function to apply the closest_topic function to each element of a 'topics' column (assigning a standard topic to facilitate comparison)

   
    def apply_closest_topic(self, text):
        # Load spaCy's English model
        nlp = spacy.load('en_core_web_lg')

        # Define predefined list of topics
        topics = ['business news', 'france news', 'england news', 'germany news', 'america news', 
              'russia news', 'politics news', 'science news', 'environment news', 'domestic news']

         #if the input is a list:      
        if type(text) == list:
              new_topic = []
              for t in text:
                    doc = nlp(t)
                    #only calculating similarity score if the document has a vector 
                    if doc.has_vector:
                           sim = [doc.similarity(nlp(tt)) for tt in topics]
                           new_topic.append(topics[np.argmax(sim)])
              return new_topic
                
        else:
               text = str(text)
               # Convert the text to a spaCy doc object
               doc = nlp(text)
               
               # Calculate the similarity scores between the text and each topic
               sim_scores = [doc.similarity(nlp(topic)) for topic in topics]
               
               # Return the topic with the highest similarity score
               closest_topic = topics[np.argmax(sim_scores)]
               
               return closest_topic


       

           