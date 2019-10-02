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

unique_votes_df = votes_df.filter(
  items=['AanestysId', 'IstuntoPvm', 'IstuntoVPVuosi', 'AanestysMitatoity', 'KohtaKasittelyVaihe', 'AanestysValtiopaivaasia'],
).rename(columns={
  'AanestysId': 'vote_id',
  'IstuntoPvm': 'date',
  'IstuntoVPVuosi': 'year',
  'AanestysMitatoity': 'annulled',
  'KohtaKasittelyVaihe': 'hearing_stage'
}).drop_duplicates()

def distribution_from_row(vote):
  return({
    'group': vote.Ryhma,
    'type': vote.Tyyppi,
    'vote_counts': {
      'for': int(vote.Jaa),
      'against': int(vote.Ei),
      'empty': int(vote.Tyhjia),
      'away': int(vote.Poissa)
    }
  })

def combine_distribution_to_vote(vote):
  distribution_rows = votes_df[votes_df.AanestysId == vote]
  distributions = {
    'distr': []
  }

  distribution_rows.apply(lambda x: distributions['distr'].append(distribution_from_row(x)), axis=1)

  return(str(distributions))

unique_votes_df = unique_votes_df.merge(proposals_df, left_on='AanestysValtiopaivaasia', right_on='id', how='left').assign(distribution=lambda x: x.vote_id)
unique_votes_df.distribution = unique_votes_df.distribution.apply(lambda x: combine_distribution_to_vote(x))

unique_votes_df = unique_votes_df.sort_values(by=['date'], ascending=False)

unique_votes_df.to_json('./data/votes_keywords_distributions.json', orient='records')
