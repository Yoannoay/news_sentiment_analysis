import datetime 
import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Analyser:

    def __init__(self, option):
        self.df = self.csvs_2_df()
        if option == "1":
            self.topic_sentiment_stckd_bar_chart()

    #getting the all the data available for the current month and putting it into a dataframe. 
    def csvs_2_df(self):
        #getting the folder name which data of the current month is added to, in order to iterate through and get the file names that exist currently
        today= datetime.datetime.now()

        directory = f"Sky_News_Articles_{today.month}_{today.year}"

        encoded_directory = os.fsencode(directory)

        list_of_csvs = []
        #adding the file path of each file which exists in this months folder, to a list 
        for file in os.listdir(encoded_directory):
            csv = os.fsdecode(file)
            filepath = os.path.join(directory, csv)
            list_of_csvs.append(filepath)
        #using the list we just created to create a dataframe using the csv data of files in the list. 
        df = pd.concat(
            map(pd.read_csv, list_of_csvs), ignore_index = True)
        

        #adding a sentiment column for each article (More positive/more negative)
        analyzer = SentimentIntensityAnalyzer()
        pos_or_neg = []
        for article in df["Article"]:
              sentiment = analyzer.polarity_scores(article)
              if sentiment["compound"] > 0:
                  pos_or_neg.append("More positive")    
              else:
                  pos_or_neg.append("More negative")

        df["Sentiment"] = pos_or_neg
        
        return df 
    
    def topic_sentiment_stckd_bar_chart(self):

        #get a list of the unique topics in the topic column.

        topics = self.df['Topics'].astype(str).unique()

        


        #trying to get the amount of negative and positive articles with the topic name. 


        positive = []
        negative = []

        for topic in topics:
            result = self.df.query("Topics == @topic")["Sentiment"]
            positive_count = 0
            negative_count = 0

            for sentiment in result:
                if sentiment == "More positive":
                    positive_count += 1
                elif sentiment == "More negative":
                    negative_count += 1

            positive.append(positive_count)
            negative.append(negative_count)


        #creating a stacked bar chart 
        fig, ax = plt.subplots()
        ax.bar(topics, positive, label= 'Positive', color='green')
        ax.bar(topics,negative, label='Negative', color='red', bottom=positive)
        ax.legend()


        #rotating x-axis labels
        plt.xticks(rotation=27)

        #making fotn smaller
        plt.xticks(fontsize=6)

        #setting chart title and axis labels 
        ax.set_title('Sentiment by Topic')
        ax.set_xlabel('Topics')
        ax.set_ylabel('Number of Articles')

        #save chart with date 
        today= datetime.datetime.now()
        foldername = "Matplotlib_Visuals\Sentiment_by_topic"
        filename = f"{today.day}_{today.month}_{today.year}_sentiment_by_topic"
        filepath = os.path.join(foldername, filename)

        #saving the dataframe as a csv to the folder. 
        if not os.path.exists(filepath):
            plt.savefig(filepath)


        

        

        

