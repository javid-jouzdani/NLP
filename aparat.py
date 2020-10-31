# Import package
import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import normalize

n_features = 100
n_topics = 2
n_top_words = 2

# Assign URL to variable: url
url = 'http://www.aparat.com/etc/api/mostViewedVideos'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Decode the JSON data into a dictionary: json_data
json_data = r.json()

# Convert to DataFrame
df = pd.DataFrame(json_data['mostviewedvideos'])

# Sort by views
df_sorted_by_views = df.sort_values(by='visit_cnt', ascending = False)

# Extract titles
titles = df_sorted_by_views['title']
print(titles)

# Construct a the TfidfVectorizer and NMF instances
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features)
nmf = NMF(n_components=20)

# Fit and transform the titles
tfidf = vectorizer.fit_transform(titles)
nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)

# Getting the features names and display the topics
feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()