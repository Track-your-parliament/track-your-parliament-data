import urllib.request, json
import pandas as pd

baseUrl = 'https://avoindata.eduskunta.fi/api/v1/tables/VaskiData'
parameters = 'rows?columnName=Eduskuntatunnus&columnValue=LA%25&perPage=100'
page = 0
df = ''

while True:
    print(f'Fetching page number {page}')
    with urllib.request.urlopen(f'{baseUrl}/{parameters}&page={page}') as url:

        data = json.loads(url.read().decode())

        if page == 0:
            columns = data['columnNames']
            df = pd.DataFrame(columns=columns)

        dataRows = data['rowData']
        df = df.append(pd.DataFrame(dataRows, columns=data['columnNames']), ignore_index=True)

        if data['hasMore'] == False:
            break

        page = page + 1

df.to_csv('./data/parliament_proposals_raw.csv', sep=';', encoding='utf-8')