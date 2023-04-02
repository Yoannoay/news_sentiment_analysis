import datetime 
import pandas as pd 
import time
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import streamlit as st 
from Analysis import Analyser
import plotly_express as px
import plotly.graph_objects as go
import spacy
import numpy as np





#page set up

st.set_page_config(page_title="News Sentiment Analysis", page_icon="🗞", layout="wide")

st.header('News Sentiment Analysis 📰')

st.text(f'''Explore sentiment analysis on four different international news sources with this web app. The app features three different visualizations:

- A histogram that shows the distribution of positive and negative articles across each news source,
- A line graph that tracks the daily changes in positive articles,
- A heatmap that highlights the degree of polarity in each news source's coverage of various topics.

The web app was inspired by the desire to showcase the different perspectives presented by news sources from different countries.
All data has been scraped, cleaned, and visualized by, Yoan Caboste.
''')




#creating table to work with
df = pd.read_csv("Complete_news_data.csv")
#getting rid of duplicate values in both the titles and the articles (only unique values can stay)
df.drop_duplicates(inplace=True)
df = df[~df['title'].duplicated(keep=False)]
df = df[~df['article'].duplicated(keep=False)]



# ------ SIDEBAR ------

st.sidebar.header("Filter By:")

news_source = st.sidebar.multiselect(
        "Choose your News source(s):",
        options=df["news_source"].unique(),
        default=df["news_source"].unique()
)


date = st.sidebar.multiselect(
        "Choose your Dates:",
        options=df["date"].unique(),
        default=df["date"].unique()
)



topic = st.sidebar.multiselect(
        "Choose your topics:",
        options=df["standardised_topic"].unique(),
        default=df["standardised_topic"].unique()
)



df_selection = df.query(
        "news_source == @news_source & date == @date & standardised_topic == @topic"
)



#SENTIMENT ANALYSIS BAR CHART: POSITIVE VS NEGATIVE


an_agent = Analyser(df_selection)
sentiment_analysis = an_agent.sentiment_analysis()

#need to get the count of articles per news source

news_source_counts = sentiment_analysis.groupby(['news_source', 'sentiment', 'topic']).count()['article'].reset_index()

news_source_counts.rename(columns={'article': 'articles'}, inplace=True)




#create a color map for plotly

color_map = {'Skewed positive' : 'green', 'Skewed negative': 'red'}
#with this extracted dataframe im going to try and make as simple a chart as I can 

sentiment_bar = px.histogram(news_source_counts, x = 'news_source', y='articles',
                        color='sentiment', barmode='group',
                        height=400, color_discrete_map=color_map,
                        title="<b>Sentiment Skew by News Source</b>")




#SENTIMENT ANALYSIS LINE PLOT: SENTIMENT OVER TIME


# Group the data by date and news source, and count the number of rows for each group
grouped_df = sentiment_analysis.groupby(['date', 'news_source', 'sentiment']).size().reset_index(name='count')

# Pivot the grouped data to get the sentiment counts as separate columns
pivoted_df = grouped_df.pivot(index=['date', 'news_source'], columns='sentiment', values='count').reset_index()

# Calculate the total count of articles for each date and news source
pivoted_df['total'] = pivoted_df['Skewed positive'] + pivoted_df['Skewed negative']

# Calculate the percentage of Skewed Positive articles for each date and news source
pivoted_df['percent_skewed_positive'] = pivoted_df['Skewed positive'] / pivoted_df['total']

# Plot the percentage of Skewed Positive articles over time, grouped by news source
sentiment_line = px.line(pivoted_df, x='date', y='percent_skewed_positive', color='news_source', title='Percentage of Skewed Positive Articles by News Source')


#SENTIMENT BY TOPIC

#grouping polarity by news source and topic
sources = sentiment_analysis.groupby(["news_source", "standardised_topic"])["polarity"].apply(list).reset_index()

grouped = pd.DataFrame(sources)


#creating new column with the avg polarity by group
grouped["avg_polarity_by_topic"] = grouped["polarity"].apply(lambda x: sum(x) / len(x))

#pivoting table
heat_pivot_table = grouped.pivot(index='news_source', columns='standardised_topic', values='avg_polarity_by_topic')

#setting up heatmap
sentiment_heat = px.imshow(heat_pivot_table, color_continuous_scale=["red", "white", "green"], 
                labels = dict(x="Topics", y = "News Source", color= "Polarity (1 = Positive, -1 = Negative)") )



#SENTIMENT TABS
sentiment_bar_tab, sentiment_line_tab, sentiment_heat_tab = st.tabs(["Sentiment by Source:bar_chart:", "Sentiment by Time📈", "Sentiment by Topic👁"])
st.markdown('##')

with sentiment_bar_tab:
        st.header("Summary of Sentiment Analysis")
        st.plotly_chart(sentiment_bar, use_container_width=True)

with sentiment_line_tab:
        st.header("Sentiment fluctuation over Time")
        st.plotly_chart(sentiment_line, use_container_width=True)

with sentiment_heat_tab:
        st.header("Polarity of Sentiment based on topic")
        st.plotly_chart(sentiment_heat, use_container_width=True)


