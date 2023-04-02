#In here I want to clean the csv a lil, return a new csv to go into a new folder

import pandas as pd
import os 
import csv
import datetime
import re 


class Cleaner:
    
    def __init__(self, csv):
       
      
       self.df = pd.read_csv(csv, sep=',')
       self.csv = csv

       
       

       #These functions should return a clean dataframe to be stored in the database. 
   
    def sky_create_topic_col(self):
       topics = []

       # Extract the second item from each list in the 'Title' column and store it as a string in the 'topics' column
       for lst in self.df['title'].str.split('|'):
          if len(lst) >= 2:
             topics.append(lst[1])
          else:
             topics.append('')
             
       self.df['topic'] = topics
       #os.remove(self.csv)

       self.df.to_csv(self.csv, index=False)



   
    def cbs_cleaner(self):
       
       #getting rid of rows with nan values.
       self.df = self.df.dropna()

       articles = []

       pattern = r"\n\s*\n\s*/\s*(.*?)\n\s*\n"

       for article in self.df["article"]:
          match = re.search(pattern, article, re.DOTALL)
          if match:
             extracted_text = match.group(1)
             extracted_text = re.sub(r"\n\s+", " ", extracted_text).strip()
             extracted_text.replace(',', '')
             extracted_text.replace('"', '')
             articles.append(extracted_text)



          else:
             articles.append(article)

    
          

       self.df["article"] = articles
       

       self.df.to_csv(self.csv, index=False)




    def dw_cleaner(self):
       #dropping anything with null values. 
       self.df = self.df.dropna()

      #checking if the article has the days date in the title, if it doesnt it is  dropped. 
       today = datetime.datetime.now()
       day = today.day
       month = today.strftime('%m')
       year = today.year
       today_str = f"{month}/{day}/{year}"
       

       

       for index, row in self.df.iterrows():
        title = row["title"]
        article_date  = title.split(" - ")[-1]


      #   if today_str not in title:
      #       self.df = self.df.drop(index)

      #getting rid of the date in the title, dont need it. 

       self.df["title"] = self.df["title"].apply(lambda x: x.split("-")[0].strip())



      #returning the data to the csv. 
       self.df.to_csv(self.csv, index = False)
      
      

    