import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud


FILE = "./20190922_090538_lemmatized_cleaned_parsed.csv"

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

# TFIDF
vectorizer = TfidfVectorizer(use_idf=True)
tfidf = vectorizer.fit_transform(df["sisalto"])

# Print top 20 for DOCUMENT = X
DOCUMENT = 200
df_tfidf = pd.DataFrame(tfidf[DOCUMENT].T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
print(df_tfidf.sort_values(by=["tfidf"], ascending=False).head(20))

# Draw wordcloud
w = WordCloud(
    background_color="white", contour_width=3, contour_color="steelblue", width=1000, height=1000
).generate_from_frequencies(df_tfidf.sort_values(by=["tfidf"], ascending=False).head(40).to_dict()["tfidf"])
print(df["nimike"].iloc[DOCUMENT])
plt.figure(figsize=(10, 10))
plt.imshow(w, interpolation="bilinear")
plt.axis("off")

