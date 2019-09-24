import pandas as pd

dataVotesDist = pd.read_csv(
    '/Users/Pete/Projects/IDS/track-your-parliament-data/SaliDBAanestysJakauma_result.csv', delimiter=';', dtype={'AanestysId': int, 'Ryhma': str, 'Jaa': int, 'Ei': int, 'Tyhjia': int, 'Poissa': int, 'Yhteensa': int, 'Tyyppi': str})
dataVoteInfos = pd.read_csv(
    '/Users/Pete/Projects/IDS/track-your-parliament-data/SaliDBAanestys_result.csv', delimiter=';', dtype={'AanestysId': int, 'IstuntoVPVuosi': int, 'IstuntoPvm': str, 'AanestysMitatoity': int, 'KohtaKasittelyVaihe': str})
dataVotesDist = dataVotesDist.drop(columns=['JakaumaId', 'Imported'])

# Filter rows
filteredVoteInfos = dataVoteInfos[(
    dataVoteInfos.KieliId == 1) & (dataVoteInfos.IstuntoVPVuosi >= 2015) & (dataVoteInfos.AanestysValtiopaivaasia.str.startswith('HE'))]
filteredVotesDist = dataVotesDist[(dataVotesDist.Tyyppi == 'eduskuntaryhma') | (
    dataVotesDist.Tyyppi == 'hallitusoppositio')]

# Drop useless columns
filteredVoteInfos = filteredVoteInfos.drop(dataVoteInfos.columns.difference(
    ['AanestysId', 'IstuntoVPVuosi', 'IstuntoPvm', 'AanestysMitatoity', 'KohtaKasittelyVaihe']), axis=1)

# Filter rows from the first voting of the year 2015
filteredVotesDist = filteredVotesDist[filteredVotesDist.AanestysId >= 36087]

joined = filteredVotesDist.merge(filteredVoteInfos, how='left', on='AanestysId')
print(joined)
