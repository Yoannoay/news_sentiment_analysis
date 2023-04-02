from plotly import graph_objects as go 
import plotly_express as px
import pandas as pd
import psycopg2
import psycopg2.extras
from Analysis import Analyser
import spacy
import numpy as np




#here i am trying to get the code to create the visualisation clean before i go ahead and put it into streamlit. 
#i'm doing this before I do the further analysis as I believe it'll give me the base to build the analysis onto. 

#getting all the data from the postgres table

def create_table():
        conn = psycopg2.connect(host='localhost', database='world_news',
                                user='postgres', password ='supremeoverlordYC7')
        cur = conn.cursor()

        sky_table = "SELECT * FROM sky_news"
        cbs_table = "SELECT * FROM cbs_news"
        dw_table = "SELECT * FROM dw_news"
        lemonde_table = "SELECT * FROM lemonde_news"

        sky_df = pd.read_sql(sky_table, conn)
        cbs_df = pd.read_sql(cbs_table, conn)
        dw_df = pd.read_sql(dw_table, conn)
        lemonde_df = pd.read_sql(lemonde_table, conn)

        df = pd.concat([sky_df, cbs_df, dw_df, lemonde_df], ignore_index=True)

        return df 
        conn.close()

df = create_table()
#making sure there arent any duplicates
df.drop_duplicates(inplace=True)
df = df[~df['title'].duplicated(keep=False)]
df = df[~df['article'].duplicated(keep=False)]


# standardising the topics to a predefined list to make comparison more uniform. 
# import spacy
# import numpy as np
# import pandas as pd

# # Load spaCy's English model
# nlp = spacy.load('en_core_web_lg')

# # Define your predefined list of topics
# topics = ['politics news', 'sports news', 'entertainment news', 'technology news', 'business news', 'world news', 'domestic news']

# # Define a function to find the closest topic to a given list of words
# def closest_topic(topic_list):
#     # Compute the average vector representation of the words in the list
#     topic_vec = np.mean([nlp(word).vector for word in topic_list], axis=0)
    
#     # Compute the cosine similarity between the topic vector and the predefined topic vectors
#     sim = [np.dot(topic_vec, nlp(topic).vector) / (np.linalg.norm(topic_vec) * np.linalg.norm(nlp(topic).vector)) for topic in topics]
    
#     # Return the topic with the highest similarity
#     return topics[np.argmax(sim)]

# # Define a function to apply the closest_topic function to each element of a 'topics' column
# def apply_closest_topic(topic):

    
#     if type(topic) == list:
#         new_topic = []
#         for t in topic:
#             doc = nlp(t)
#             sim = [doc.similarity(nlp(tt)) for tt in topics]
# #             new_topic.append(topics[np.argmax(sim)])
# #         return new_topic
# #     else:
# #         doc = nlp(topic)
# #         sim = [doc.similarity(nlp(tt)) for tt in topics]
# #         return topics[np.argmax(sim)]



# # # Apply the closest_topic function to the 'topics' column
# # df['standardised_topic'] = df['topic'].apply(apply_closest_topic)
# # # print(df[['title', 'topic']])
# # print(df.describe())
# # # sample_topics = ['politics', 'sports', 'music', 'concert']
# # # print(apply_closest_topic(sample_topics))  # Output: 'entertainment'






# # #giving the df to the analyser class so that it may convert it/append the necessary analysis, in this case sentiment analysis

# # an_agent = Analyser(df)
# # sentiment_analysis = an_agent.sentiment_analysis()

# # #need to get the count of articles per news source

# # news_source_counts = sentiment_analysis.groupby(['news_source', 'sentiment', 'topic']).count()['article'].reset_index()
# # news_source_counts.rename(columns={'article': 'count'}, inplace=True)


# # #create a color map for plotly

# # color_map = {'More positive' : 'green', 'More negative': 'red'}
# # #with this extracted dataframe im going to try and make as simple a chart as I can 

# # test_fig = px.histogram(news_source_counts, x = 'news_source', y='count',
# #                         color='sentiment', barmode='group',
# #                         height=400, color_discrete_map=color_map, facet_col='topic')

# # test_fig.show()


# #I think I might just have to make a column with 



# ##testing time series 

# an_agent = Analyser(df)
# sentiment_analysis = an_agent.sentiment_analysis()


# # Define the filter condition
# filter_cond = (sentiment_analysis['sentiment'] == 'Skewed positive') | (df['sentiment'] == 'Skewed negative')

# # Filter the data based on the condition
# filtered_df = sentiment_analysis[filter_cond]

# # Group the filtered data by date and news source, and count the number of rows for each group
# grouped_df = filtered_df.groupby(['date', 'news_source', 'sentiment']).size().reset_index(name='count')

# # Pivot the grouped data to get the sentiment counts as separate columns
# pivoted_df = grouped_df.pivot(index=['date', 'news_source'], columns='sentiment', values='count').reset_index()

# # Calculate the total count of articles for each date and news source
# pivoted_df['total'] = pivoted_df['Skewed positive'] + pivoted_df['Skewed negative']

# # Calculate the percentage of Skewed Positive articles for each date and news source
# pivoted_df['pct_skewed_pos'] = pivoted_df['Skewed positive'] / pivoted_df['total']

# # Plot the percentage of Skewed Positive articles over time, grouped by news source
# fig = px.line(pivoted_df, x='date', y='pct_skewed_pos', color='news_source', title='Percentage of Skewed Positive Articles by News Source')
# fig.show()



#Surface plot attempt. 

#god my head is a lil scrambled, the three dimensions are sentiment(polarity or percentage), news source and topic 
#i think im going to go with polarity and see what it gives. 
# def apply_closest_topic(topic):
    
#     # Load spaCy's English model
#         nlp = spacy.load('en_core_web_lg')

#         # Define your predefined list of topics
#         topics = ['politics news', 'sports news', 'entertainment news', 'technology news', 'business news', 'world news', 'domestic news']

    
#         if type(topic) == list:
#                 new_topic = []
#                 for t in topic:
#                         doc = nlp(t)
#                         sim = [doc.similarity(nlp(tt)) for tt in topics]
#                         new_topic.append(topics[np.argmax(sim)])
#                         return new_topic
#         else:
#                 doc = nlp(topic)
#                 sim = [doc.similarity(nlp(tt)) for tt in topics]
#                 return topics[np.argmax(sim)]
# def standardise_topics(df):
#         df['standardised_topic'] = df['topic'].apply(apply_closest_topic)

#         return df
# df = standardise_topics(df=df)

# df.to_csv('stnd_data.csv', index=False)

# Aggregate count column by summing
# grouped_df = grouped_df.groupby(["news_source", "topic", "polarity"]).sum().reset_index()

# pivoted_df = grouped_df.pivot(index=['topic', 'news_source'], columns='polarity', values='count').reset_index()
# pivoted_df['total'] = grouped_df.groupby(['topic', 'news_source'])['article'].nunique().values

# grouped_df = sentiment_analysis.groupby(["news_source", "topic", "polarity"]).size().reset_index(name='count')
import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np

df = pd.read_csv('stnd_data.csv')

df.drop_duplicates(inplace=True)
df = df[~df['news_source'].duplicated(keep=False)]
df = df[~df['standardised_topic'].duplicated(keep=False)]

print(df)


an_agent = Analyser(df)
sentiment_analysis = an_agent.sentiment_analysis()
sentiment_analysis = sentiment_analysis[~sentiment_analysis['polarity'].duplicated(keep=False)]



filtered_df = sentiment_analysis.pivot(index = "news_source", columns = "standardised_topic", values = "polarity")
print(sentiment_analysis)
print(filtered_df)




# data = df.groupby('news_source', 'article')['polarity'].apply(list)



# Pivot the table
# sentiment_pivot = sentiment_analysis.pivot(index='standardised_topic', columns='news_source', values='polarity')

# # Create the heatmap
# fig = px.imshow(sentiment_pivot,
#                 x=sentiment_pivot.columns,
#                 y=sentiment_pivot.index,
#                 color_continuous_scale='RdBu',
#                 zmin=-1,
#                 zmax=1)

# # Update axis labels and title
# fig.update_xaxes(title='News Source')
# fig.update_yaxes(title='Standardised Topic')
# fig.update_layout(title='Polarity Heatmap')

# # Show the plot
# fig.show()



# # Define colors for each news_source category
# colors = {'CBS News': 'rgb(31, 119, 180)',
#           'DW News': 'rgb(255, 127, 14)',
#           'LeMonde News': 'rgb(44, 160, 44)',
#           'Sky News': 'rgb(214, 39, 40)'}

# # Create a list of violins, one for each news_source category
# violins = []
# for news_source, polarity in sentiment_analysis.items():
#     violins.append(go.Violin(y=polarity, name=news_source, line_color=colors[news_source]))

# # Create the plot
# fig = go.Figure(violins)
# fig.update_layout(title='Polarity by News Source', yaxis_title='Polarity')
# fig.show()









# sentiment_analysis['polarity'] = pd.to_numeric(df['polarity'])

# surface_fig = go.Figure(data=[go.Surface(z=sentiment_analysis['polarity'], x=sentiment_analysis['news_source'], y=sentiment_analysis['standardised_topic'])])
# surface_fig.update_layout(scene = dict(xaxis_title='News Source', yaxis_title='Topic', zaxis_title='Total Count'), 
#                           autosize=False, 
#                           width=800, 
#                           height=800,
#                           margin=dict(l=65, r=50, b=65, t=90))

# surface_fig.show()



# test_fig = px.line_3d(grouped, x="standardised_topic", y="news_source", z="polarity")

# test_fig.show()

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=sentiment_analysis["news_source"], y=sentiment_analysis["topic"],
#                           mode='markers', marker=dict(size=sentiment_analysis["polarity"], sizemode='area')))


# import plotly.express as px

# fig1 = px.scatter(sentiment_analysis, x="news_source", y="standardised_topic", size="polarity", color="polarity", 
#                  hover_data=["hover_column"], color_continuous_scale=px.colors.diverging.RdYlGn)

# fig = go.Figure(data=go.Scatter3d(
#     x=sentiment_analysis['news_source'],
#     y=sentiment_analysis['standardised_topic'],
#     z=sentiment_analysis['polarity'],
#     mode='markers',
#     marker=dict(
#         size=10,
#         color=df['polarity'],
#         colorscale='Viridis',
#         opacity=0.8
#     )
# ))
# fig.show()


# fig.show()



# SURFACE 

