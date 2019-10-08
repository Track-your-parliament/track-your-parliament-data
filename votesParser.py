import pandas as pd
import time

PATH_DIST = './data/SaliDBAanestysJakauma_result.csv'
PATH_VOTES = './data/SaliDBAanestys_result.csv'

dataVotesDist = pd.read_csv(
    PATH_DIST,
    delimiter=';', 
    dtype={'AanestysId': int, 'Ryhma': str, 'Jaa': int, 'Ei': int, 'Tyhjia': int, 'Poissa': int, 'Yhteensa': int, 'Tyyppi': str})
dataVoteInfos = pd.read_csv(
    PATH_VOTES, 
    delimiter=';', 
    dtype={'AanestysId': int, 'IstuntoVPVuosi': int, 'IstuntoNumero': int, 'IstuntoPvm': str, 'AanestysMitatoity': int, 'KohtaKasittelyVaihe': str, 'AanestysValtiopaivaasia': str, 'AanestysAlkuaika': str })

# Filter rows
filteredVoteInfos = dataVoteInfos[(
    dataVoteInfos.KieliId == 1) & (dataVoteInfos.IstuntoVPVuosi >= 2015) & (dataVoteInfos.AanestysValtiopaivaasia.str.startswith('HE'))]
filteredVotesDist = dataVotesDist[(dataVotesDist.Tyyppi == 'eduskuntaryhma') | (
    dataVotesDist.Tyyppi == 'hallitusoppositio')]

# Drop useless columns
filteredVoteInfos = filteredVoteInfos.drop(dataVoteInfos.columns.difference(
    ['AanestysId', 'IstuntoVPVuosi', 'IstuntoNumero', 'IstuntoPvm', 'AanestysMitatoity', 'KohtaKasittelyVaihe', 'AanestysValtiopaivaasia', 'AanestysAlkuaika']), axis=1)
filteredVotesDist = filteredVotesDist.drop(columns=['JakaumaId', 'Imported'])

# Filter rows from the first voting of the year 2015
filteredVotesDist = filteredVotesDist[filteredVotesDist.AanestysId >= 36087]

# Every other votingId refers to the previous voting på svenska
#print(filteredVotesDist[filteredVotesDist.AanestysId == 36088])

# Join the two tables with merge, remove rows with NaNs.
joined = filteredVotesDist.merge(filteredVoteInfos, how='left', on='AanestysId')
joined = joined.dropna(axis=0)
joined = joined[(joined.KohtaKasittelyVaihe == 'Ainoa käsittely')
    | (joined.KohtaKasittelyVaihe == 'Toinen käsittely')
    | (joined.KohtaKasittelyVaihe == 'Toinen käsittely, ainoa käsittely')
    | (joined.KohtaKasittelyVaihe == 'Osittain ainoa, osittain toinen käsittely')]

# Save file
joined.to_csv('./data/voting_info.csv', sep=';')