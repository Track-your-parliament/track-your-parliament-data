import pandas as pd
import numpy as np
import json

PROPOSALS = './data/proposals_with_keywords.json'
VOTE_DISTRIBUTIONS = './data/voting_info.csv'
HEARINGS = {
  'Ainoa käsittely': 'Only hearing',
  'Toinen käsittely': 'Second hearing',
  'Toinen käsittely, ainoa käsittely': 'Second hearing, only hearing',
  'Osittain ainoa, osittain toinen käsittely': 'Partly only hearing, partly second hearing'
}

proposals_df = pd.read_json(PROPOSALS)

votes_df = pd.read_csv(VOTE_DISTRIBUTIONS, ';').drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
votes_df = votes_df[votes_df.AanestysValtiopaivaasia.isin(proposals_df.id.unique())]

votes_df = votes_df.merge(proposals_df, left_on='AanestysValtiopaivaasia', right_on='id', how='left')
votes_df.to_json('./data/votes_keywords_distributions.json', orient='records')
