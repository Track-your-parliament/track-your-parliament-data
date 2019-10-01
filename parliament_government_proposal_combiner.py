import pandas as pd

GOVERNMENT_PROPOSALS = './data/government_proposals_clean.csv'
PARLIAMENT_PROPOSALS = './data/parliament_proposals_clean.csv'

gov_proposals = pd.read_csv(GOVERNMENT_PROPOSALS, ';')
parl_proposals = pd.read_csv(PARLIAMENT_PROPOSALS, ';')

all_proposals = gov_proposals.append(parl_proposals, sort=False)

all_proposals.to_csv('./data/proposals_clean.csv', ';')
