import urllib.request, json
import pandas as pd

PROPOSALS = './data/votes_keywords_distributions.json'

BASE_URL = 'https://avoindata.eduskunta.fi/api/v1/tables/SaliDBKohta'
PARAMETERS = 'rows?columnName=PJKohtaTunnus&perPage=100&page=0'

# Find the correct session for the vote and store session ID and decision
def set_session_to_row(row, session_data):
    gathering_id = f'{row.year}/{row.gathering_number}'

    dataRows = pd.DataFrame(session_data['rowData'], columns=session_data['columnNames'])
    dataRows = dataRows[dataRows.IstuntoTekninenAvain == gathering_id].sort_values(by=['Id'], ascending=False)

    if dataRows.TekninenAvain.count() != 0:
        row.session = dataRows.TekninenAvain.values[0]
        row.decision = dataRows.PaatosFI.values[0]

    return row


# Find the sessions for a document
def fetch_session_info(row):

    proposal_id = row.id.replace(' ', '+').replace('/', '%2F').lower()
    columnValue = f'&columnValue={proposal_id}'

    with urllib.request.urlopen(f'{BASE_URL}/{PARAMETERS}{columnValue}') as url:

        data = json.loads(url.read().decode())
        return set_session_to_row(row, data)

df = pd.read_json(PROPOSALS)

# Add new columns for session information
df = df.assign(session='')
df = df.assign(decision='')

df = df.apply(lambda x: fetch_session_info(x), axis=1)
grouped_votes = df.groupby(by=['session'])

def get_session_for_vote_group(vote_group):
    return {
        'session': vote_group.session.values[0],
        'decision': vote_group.decision.values[0],
        'id': vote_group.id.values[0],
        'summary': vote_group.summary.values[0],
        'year': int(vote_group.year.values[0]),
        'title': vote_group.title.values[0],
        'created': vote_group.created.values[0],
        'keywords': vote_group.keywords.values[0],
        'keyword_list': vote_group.keywords_list.values[0],
        'votes': []
    }

def get_votes_for_session(session_id):

    votes = []
    df[df.session == session_id].apply(lambda x: votes.append({
        'vote_id': int(x['vote_id']),
        'time': x['time'],
        'annulled': x['annulled'],
        'distribution': x['distribution']
    }), axis=1)

    return votes

def group_votes_by_sessions(dataFrame):
    session_votes = []

    for group in grouped_votes.groups:
        vote_group = grouped_votes.get_group(group)

        session = get_session_for_vote_group(vote_group)
        session['votes'] = get_votes_for_session(session['session'])

        session_votes.append(session)

    return session_votes

votes_by_session = group_votes_by_sessions(df)

with open('./data/votes_with_sessions.json', 'w') as out:
    json.dump(votes_by_session[1:], out)
