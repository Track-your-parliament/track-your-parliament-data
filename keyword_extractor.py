import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import json

FILE = "./data/20190924_141345_lemmatized_cleaned_parsed.csv"
documents = []

df = pd.read_csv(FILE, ";")

# Drop junk columns
df = df.drop(df.columns[0:2], axis=1)

# Drop rows which have no "sisalto" for any level
df.dropna(how="all", axis=0, subset=df.columns[-8:], inplace=True)


def combine(row, columns):
    items = [row[column] for column in columns]
    items = filter(lambda x: isinstance(x, str) and len(x) > 0, items)
    return " ".join(items)


# Combine sisalto from all levels to one column
df["sisalto"] = df.apply(lambda x: combine(x, df.columns[-8:]), axis=1)

df = df.drop(df.columns[-9:-1], axis=1)

# Create an entry for each document in the object array documents
df.apply(lambda x: documents.append({
    'id': x['Eduskuntatunnus'],
    'title': x['nimike'],
    'created': x['Created'],
    'keywords': []
  }), axis=1)

# TFIDF
vectorizer = TfidfVectorizer(use_idf=True)
tfidf = vectorizer.fit_transform(df["sisalto"])

# Extract keywords from tfidf matrix and attach top 20 to the correct document object,
# then write that object into a json file.
def extract_keywords(idx, out):
  df_tfidf = pd.DataFrame(tfidf[idx].T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
  main_keywords = df_tfidf.sort_values(by=["tfidf"], ascending=False).head(20).reset_index().rename(columns={'index': 'word'})
  main_keywords.apply(lambda x: documents[idx]['keywords'].append({ 'word': x[0], 'tfidf': x[1] }), axis=1)
  json.dump(documents[idx], out)
  if idx != len(documents) - 1:
    out.write(',\n')

with open('documents_with_keywords.json', 'w') as out:
  out.write('[')
  pd.Series(np.arange(0, len(documents))).apply(lambda x: extract_keywords(x, out))
  out.write(']')

# Draw wordcloud
# w = wordcloud.WordCloud(
#     background_color="white", contour_width=3, contour_color="steelblue", width=1000, height=1000
# ).generate_from_frequencies(df_tfidf.sort_values(by=["tfidf"], ascending=False).head(40).to_dict()["tfidf"])
# print(df["nimike"].iloc[DOCUMENT])
# plt.figure(figsize=(10, 10))
# plt.imshow(w, interpolation="bilinear")
# plt.axis("off")
