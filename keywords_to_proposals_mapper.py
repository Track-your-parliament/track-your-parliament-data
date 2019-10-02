import pandas as pd
import json

PROPOSALS = './data/proposals_with_keywords.json'

df = pd.read_json(PROPOSALS)
keywords = {}

def map_keywords_to_proposal(row):

  for keyword in row['keywords_list']:

    if keyword in keywords:
      keywords[keyword].append(row.id)
    else:
      keywords[keyword] = [row.id]

df.apply(lambda x: map_keywords_to_proposal(x), axis=1)

with open('./data/keywords_with_proposals.json', 'w') as fp:
    json.dump(keywords, fp)