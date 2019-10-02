import pandas as pd
import numpy as np
import datetime

PROPOSALS = './data/votes_keywords_distributions.json'

df = pd.read_json(PROPOSALS)
df = df.assign(year=lambda x: x.date.dt.year)
df = df.assign(month=lambda x: x.date.dt.month)
group_by_month = df.groupby(by=['year', 'month'])

monthly_keywords = df.filter(items=['year', 'month']).drop_duplicates().reset_index().drop(columns=['index'])
monthly_keywords = monthly_keywords.reset_index().rename(columns={'index': 'keywords_list'})

def get_top_keywords_for_month(month):
  month_keywords = []
  df[(df.year == monthly_keywords.year[month]) & (df.month == monthly_keywords.month[month])].keywords.apply(lambda x: month_keywords.extend(x))
  return pd.DataFrame(month_keywords).drop_duplicates().sort_values(by=['tfidf'], ascending=False).head(20).word.to_numpy()

monthly_keywords.keywords_list = monthly_keywords.keywords_list.apply(lambda x: get_top_keywords_for_month(x))

monthly_keywords = monthly_keywords.sort_values(by=['year', 'month'], ascending=False)

monthly_keywords.to_json('./data/top_keywords_by_month.json', orient='records')
