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

# def create_table():
#         conn = psycopg2.connect(host='localhost', database='world_news',
#                                 user='postgres', password ='supremeoverlordYC7')
#         cur = conn.cursor()

#         sky_table = "SELECT * FROM sky_news"
#         cbs_table = "SELECT * FROM cbs_news"
#         dw_table = "SELECT * FROM dw_news"
#         lemonde_table = "SELECT * FROM lemonde_news"

#         sky_df = pd.read_sql(sky_table, conn)
#         cbs_df = pd.read_sql(cbs_table, conn)
#         dw_df = pd.read_sql(dw_table, conn)
#         lemonde_df = pd.read_sql(lemonde_table, conn)

#         df = pd.concat([sky_df, cbs_df, dw_df, lemonde_df], ignore_index=True)

#         return df 
#         conn.close()

# df = create_table()
# #making sure there arent any duplicates
# df.drop_duplicates(inplace=True)
# df = df[~df['title'].duplicated(keep=False)]
# df = df[~df['article'].duplicated(keep=False)]



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


df = pd.read_csv("stnd_data.csv")


# print(df.columns)

an_agent = Analyser(df)


sentiment_analysis = an_agent.sentiment_analysis()
# sentiment_analysis = sentiment_analysis[~sentiment_analysis['polarity'].duplicated(keep=False)]


sources = sentiment_analysis.groupby(["news_source", "standardised_topic"])["polarity"].apply(list).reset_index()


grouped = pd.DataFrame(sources)



grouped["avg_polarity_by_topic"] = grouped["polarity"].apply(lambda x: sum(x) / len(x))

pivot_table = grouped.pivot(index='news_source', columns='standardised_topic', values='avg_polarity_by_topic')

print(pivot_table)
heatmap = grouped[["news_source", "standardised_topic", "avg_polarity_by_topic"]]

fig = px.imshow(pivot_table, color_continuous_scale=["red", "white", "green"], 
                labels = dict(x="Topics", y = "News Source", color= "Polarity (1 = Positive, -1 = Negative)") )
fig.show()


# fig = px.imshow(grouped,
#                 x='news_source',
#                 y='standardised_topic',
#                 color_continuous_scale='RdBu',
#                 zmin=-1,
#                 zmax=1)

# # Update axis labels and title
# fig.update_xaxes(title='News Source')
# fig.update_yaxes(title='Standardised Topic')
# fig.update_layout(title='Polarity Heatmap')

# # Show the plot
# fig.show()






