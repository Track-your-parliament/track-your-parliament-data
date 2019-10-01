import pandas as pd
import numpy as np
import datetime

PROPOSALS = './data/votes_keywords_distributions.json'

df = pd.read_json(PROPOSALS)
df = df.assign(Year=lambda x: x.date.dt.year)
df = df.assign(Month=lambda x: x.date.dt.month)
group_by_month = df.groupby(by=['Year', 'Month'])

monthly_tags = df.filter(items=['Year', 'Month']).drop_duplicates().reset_index().drop(columns=['index'])
monthly_tags = monthly_tags.reset_index().rename(columns={'index': 'Tags'})

def get_top_tags_for_month(month):
  month_tags = []
  df[(df.Year == monthly_tags.Year[month]) & (df.Month == monthly_tags.Month[month])].keywords.apply(lambda x: month_tags.extend(x))
  return pd.DataFrame(month_tags).drop_duplicates().sort_values(by=['tfidf'], ascending=False).head(20).word.to_numpy()

monthly_tags.Tags = monthly_tags.Tags.apply(lambda x: get_top_tags_for_month(x))

monthly_tags.to_json('./data/top_keywords_by_month.json', orient='records')
