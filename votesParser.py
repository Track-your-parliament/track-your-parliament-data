import pandas as pd

dataVotesDist = pd.read_csv(
    '/Users/Pete/Projects/IDS/track-your-parliament-data/SaliDBAanestysJakauma_result.csv', 
    delimiter=';', 
    dtype={'AanestysId': int, 'Ryhma': str, 'Jaa': int, 'Ei': int, 'Tyhjia': int, 'Poissa': int, 'Yhteensa': int, 'Tyyppi': str})
dataVoteInfos = pd.read_csv(
    '/Users/Pete/Projects/IDS/track-your-parliament-data/SaliDBAanestys_result.csv', 
    delimiter=';', 
    dtype={'AanestysId': int, 'IstuntoVPVuosi': int, 'IstuntoPvm': str, 'AanestysMitatoity': int, 'KohtaKasittelyVaihe': str})

# Filter rows
filteredVoteInfos = dataVoteInfos[(
    dataVoteInfos.KieliId == 1) & (dataVoteInfos.IstuntoVPVuosi >= 2015) & (dataVoteInfos.AanestysValtiopaivaasia.str.startswith('HE'))]
filteredVotesDist = dataVotesDist[(dataVotesDist.Tyyppi == 'eduskuntaryhma') | (
    dataVotesDist.Tyyppi == 'hallitusoppositio')]

# Drop useless columns
filteredVoteInfos = filteredVoteInfos.drop(dataVoteInfos.columns.difference(
    ['AanestysId', 'IstuntoVPVuosi', 'IstuntoPvm', 'AanestysMitatoity', 'KohtaKasittelyVaihe']), axis=1)
filteredVotesDist = filteredVotesDist.drop(columns=['JakaumaId', 'Imported'])

# Filter rows from the first voting of the year 2015
filteredVotesDist = filteredVotesDist[filteredVotesDist.AanestysId >= 36087]

# Every other votingId refers to the previous voting på svenska
#print(filteredVotesDist[filteredVotesDist.AanestysId == 36088])

# Join the two tables with merge, remove rows with NaNs.
joined = filteredVotesDist.merge(filteredVoteInfos, how='left', on='AanestysId')
joined = joined.dropna(axis=0)
print(joined.head(40))
print(joined.columns)
print(joined.Ryhma.unique())

#pivoted = joined.pivot() or joined.pivot_table() <-- more secure
