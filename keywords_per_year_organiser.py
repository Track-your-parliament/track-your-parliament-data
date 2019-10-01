import pandas as pd
import numpy as np
import datetime

PROPOSALS = './data/votes_keywords_distributions.json'

df = pd.read_json(PROPOSALS)
df = df.assign(Year=lambda x: x.date.dt.year)
group_by_years = df.groupby(by=['Year'])

yearly_tags = pd.DataFrame(df.Year.unique(), columns=['Year'])
yearly_tags = yearly_tags.assign(Tags=lambda x: x.Year)

def get_top_tags_for_year(year):
  year_tags = []
  group_by_years.get_group(year).keywords.apply(lambda x: year_tags.extend(x))
  return pd.DataFrame(year_tags).drop_duplicates().sort_values(by=['tfidf'], ascending=False).head(20).word.to_numpy()

yearly_tags.Tags = yearly_tags.Tags.apply(lambda x: get_top_tags_for_year(x))

yearly_tags.to_json('./data/top_keywords_by_year.json', orient='records')
