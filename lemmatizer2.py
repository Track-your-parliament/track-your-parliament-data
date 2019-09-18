import pandas as pd
import libvoikko
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words

LEVEL = '*/'

df = pd.read_csv('xml_parsed.csv', ';')
voikko = libvoikko.Voikko(u"fi")
stopwords = get_stop_words('finnish')
docs = []

print(df.shape)

for row in np.arange(3, 20):
    text = df.sisaltokuvaus[row]

    print(text)
    if not isinstance(text, str):
        continue

    split_no_punctuation = pd.Series(pd.Series(text).str.replace('[^\w\s]', ' ').str.split().values[0])
    lemmatized = split_no_punctuation\
        .apply(lambda x: voikko.analyze(x))\
        .apply(lambda x: x[0]['BASEFORM'] if len(x) > 0 else '')\
        .apply(lambda x: '' if x in stopwords else x)
    lemmatized_joined = ' '.join(lemmatized.values)

    if len(lemmatized_joined) > 0:

        print('--------------------------------------------------------')
        print(lemmatized_joined)
        print('--------------------------------------------------------')

        docs.append(lemmatized_joined)

vect = TfidfVectorizer(use_idf=True)
tfidf = vect.fit_transform(docs)

tfidf_df = pd.DataFrame(tfidf.T.todense(), index=[vect.get_feature_names()])

for i in np.arange(0, 10):
    print(tfidf_df.sort_values(by=[i], ascending=False).head())
