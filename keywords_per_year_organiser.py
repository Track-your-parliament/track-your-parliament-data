import pandas as pd
import numpy as np
import datetime

PROPOSALS = './data/votes_keywords_distributions.json'

df = pd.read_json(PROPOSALS)
df = df.assign(year=lambda x: x.date.dt.year)
group_by_years = df.groupby(by=['year'])

yearly_keywords = pd.DataFrame(df.year.unique(), columns=['year'])
yearly_keywords = yearly_keywords.assign(keywords_list=lambda x: x.year)

def get_top_keywords_for_year(year):
  year_keywords = []
  group_by_years.get_group(year).keywords.apply(lambda x: year_keywords.extend(x))
  return pd.DataFrame(year_keywords).drop_duplicates().sort_values(by=['tfidf'], ascending=False).head(20).word.to_numpy()

yearly_keywords.keywords_list = yearly_keywords.keywords_list.apply(lambda x: get_top_keywords_for_year(x))

yearly_keywords = yearly_keywords.sort_values(by=['year'], ascending=False)

yearly_keywords.to_json('./data/top_keywords_by_year.json', orient='records')
