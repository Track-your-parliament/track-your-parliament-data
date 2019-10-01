import pandas as pd
import numpy as np
import datetime

PROPOSALS = './data/votes_keywords_distributions.json'

df = pd.read_json(PROPOSALS)
daily_keywords = df.filter(items=['date']).drop_duplicates().reset_index().drop(columns=['index'])
daily_keywords = daily_keywords.reset_index().rename(columns={'index': 'keywords_list'})

def get_top_keywords_for_day(day):
  day_keywords = []
  df[df.date == daily_keywords.date[day]].keywords.apply(lambda x: day_keywords.extend(x))
  return pd.DataFrame(day_keywords).drop_duplicates().sort_values(by=['tfidf'], ascending=False).head(20).word.to_numpy()

daily_keywords.keywords_list = daily_keywords.keywords_list.apply(lambda x: get_top_keywords_for_day(x))
daily_keywords.date = daily_keywords.date.astype(str)

daily_keywords.to_json('./data/top_keywords_by_day.json', orient='records')
