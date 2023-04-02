import datetime 
import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Analyser:

    def __init__(self, df):
        self.df = df


    #getting the all the data available for the current month and putting it into a dataframe. 
    def sentiment_analysis(self):
        
        #adding a sentiment column for each article (More positive/more negative)
        analyzer = SentimentIntensityAnalyzer()
        pos_or_neg = []
        compound = []
        for article in self.df["article"]:
              
              sentiment = analyzer.polarity_scores(article)
              compound.append(sentiment['compound'])
              if sentiment["compound"] > 0.01:
                  pos_or_neg.append("Skewed positive")    
              else:
                  pos_or_neg.append("Skewed negative")

        self.df["sentiment"] = pos_or_neg
        self.df["polarity"] = compound

        return self.df 
    