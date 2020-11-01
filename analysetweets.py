#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:00:58 2020

@author: javid
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from textblob import TextBlob
import json

tweets_data_path = 'tweets.txt'

n_features = 5000
n_topics = 50
n_top_words = 50

# Initialize empty list to store tweets: tweets_data
tweets_data = []

# Open connection to file
tweets_file = open(tweets_data_path, "r")

# Read in tweets and store in list: tweets_data
for line in tweets_file:
    tweet = json.loads(line)
    tweets_data.append(tweet) 

# Close connection to file
tweets_file.close()

# Build DataFrame of tweet texts and languages
df = pd.DataFrame(tweets_data, columns=['text', 'lang'])

# Print head of DataFrame
print(df.head())

# Extract tweets
tweets = df[df.lang == 'en']['text']

# Construct a Pipeline by a TfidfVectorizer and NMF
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                        stop_words='english')
tfidf = vectorizer.fit_transform(tweets)
nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)

# Getting the features names and display the topics
feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    topic_words = " ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]])
    blob = TextBlob(topic_words)
    print(blob)
    print(blob.sentiment)
    print()
    
#res_df = pd.DataFrame(columns=['Indx', 'Who', 'Polarity', 'Subjectivity'])
row_list = []
for topic_idx, topic in enumerate(nmf.components_):
    topic_words = " ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]])
    blob = TextBlob(topic_words)
    if ('trump' in topic_words) or ('Trump' in topic_words):
        dict1 = ['Trump', blob.sentiment[0], blob.sentiment[1]]
    elif ('biden' in topic_words)  or ('Biden' in topic_words):        
        dict1 = ['Biden', blob.sentiment[0], blob.sentiment[1]]
    else:
        dict1 = ['N/A', blob.sentiment[0], blob.sentiment[1]]
    row_list.append(dict1)

res_df = pd.DataFrame(row_list, columns=['Who', 'Polarity', 'Subjectivity'])
print(res_df.groupby('Who').agg(['mean', 'count']))
