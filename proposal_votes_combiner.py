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

votes_df = pd.read_csv(VOTE_DISTRIBUTIONS, ';')
grouped_votes_by_proposal = votes_df.groupby(by=['AanestysValtiopaivaasia'])

proposals_df = pd.read_json(PROPOSALS)
proposals_df = proposals_df[proposals_df.id.isin(votes_df.AanestysValtiopaivaasia.unique())]

def vote_from_vote_group(vote_group):
  return({
    'vote_id': vote_group.AanestysId.values[0],
    'date': vote_group.IstuntoPvm.values[0],
    'year': int(vote_group.IstuntoVPVuosi.values[0]),
    'annulled': vote_group.AanestysMitatoity.values[0] == 1,
    'hearing_stage': HEARINGS[vote_group.KohtaKasittelyVaihe.values[0]],
    'distribution': []
  })

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

def combine_votes_to_proposal(proposal):
  votes_group = grouped_votes_by_proposal.get_group(proposal)
  grouped_votes_by_id = votes_group.groupby(by=['AanestysId'])
  votes = []

  for group in grouped_votes_by_id.groups:
    vote_group = grouped_votes_by_id.get_group(group)
    vote = vote_from_vote_group(vote_group)
    votes.append(vote)

    vote_group.apply(lambda x: vote['distribution'].append(distribution_from_row(x)), axis=1)

  return(votes)

proposals_df = proposals_df.assign(votes=lambda x: x.id)
proposals_df.votes = proposals_df.votes.apply(lambda x: combine_votes_to_proposal(x))

proposals_df = proposals_df.sort_values(by=['created'], ascending=False)

proposals_df.to_json('./data/proposals_keywords_distributions.json', orient='records')
