import pandas as pd
import xml.etree.ElementTree as ET
import libvoikko
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words

LEVEL = '*/'

df = pd.read_csv('VaskiData_result.csv', ';')
voikko = libvoikko.Voikko(u"fi")
stopwords = get_stop_words('finnish')
docs = []

for row in np.arange(3, 20):
    xml = df.XmlData[row]
    root = ET.fromstring(xml)

    text = ''
    for levelNumber in np.arange(1, 10):
        foundLevels = 0
        found = False
        level = LEVEL * levelNumber
        for item in root.findall(level + "{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}KappaleKooste"):
            if isinstance(item.text, str) and len(item.text) > 0:
                text += item.text
                found = True

        if found:
            foundLevels += 1
            if foundLevels > 2:
                break

    print(text)
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
