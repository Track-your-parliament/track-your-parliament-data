# track-your-parliament-data

Data for project Track-your-parliament

Data has been fetched and parsed from https://avoindata.eduskunta.fi and it's using "CC Nimeä 4.0" -license (*"Data on tarjolla palvelussa JHS 189 -suosituksen mukaisesti CC Nimeä 4.0 -lisenssillä"*)

`stop_words.txt` -file has been gathered from below sources:
- https://github.com/stopwords-iso/stopwords-fi
- https://github.com/Alir3z4/stop-words

### Data models

#### `proposals_keywords_distributions.json`

```
{
  id: {|Id of the proposal|},
  title: {|Title of the proposal|},
  created: {|Creation date of the proposal|},
  summary: {|Summary of the proposal|},
  keywords: [
    {
      word: {|Word in the proposal|},
      tfidf: {|TF-IDF score of the word|}
    },
    ...
  ],
  keywords_list: [
    {|Word in the proposal|},
    ...
  ],
  votes: [
    {
      vote_id: {|Id of the vote|},
      date: {|Date when vote took place|},
      year: {|Year of the vote|},
      annulled: {|1 if the vote has been annulled, 0 otherwise|},
      hearing_stage: {|Which stage the vote took place in (first/second hearing etc)|},
      distribution: [
        {
          group: {|Name of the group|}
          type: {|Type of the group (parliamentary group or opposition/government parties|}
          vote_counts: {
            for: {|Number of people in the group who voted for|},
            against: {|Number of people in the group who voted against|},
            empty: {|Number of people in the group who voted empty|},
            away: {|Number of people in the group who were absent|}
          }
        },
        ...
      ]
    },
    ...
  ]
}
```

#### `votes_keywords_distributions.json`
```
{
  vote_id: {|Id of the vote|},
  date: {|Date when vote took place|},
  year: {|Year of the vote|},
  annulled: {|1 if the vote has been annulled, 0 otherwise|},
  hearing_stage: {|Which stage the vote took place in (first/second hearing etc)|},
  distribution: [
    {
      group: {|Name of the group|}
      type: {|Type of the group (parliamentary group or opposition/government parties|}
      vote_counts: {
        for: {|Number of people in the group who voted for|},
        against: {|Number of people in the group who voted against|},
        empty: {|Number of people in the group who voted empty|},
        away: {|Number of people in the group who were absent|}
      }
    },
    ...
  ]
  id: {|Id of the proposal|},
  title: {|Title of the proposal|},
  created: {|Creation date of the proposal|},
  summary: {|Summary of the proposal|},
  keywords: [
    {
      word: {|Word in the proposal|},
      tfidf: {|TF-IDF score of the word|}
    },
    ...
  ],
  keywords_list: [
    {|Word in the proposal|},
    ...
  ]
}
```

#### `top_keywords_by_year.json`
```
{
  year: {|Year|},
  keywords_list: [
    {|word|},
    ...
  ]
}
```

#### `top_keywords_by_month.json`
```
{
  year: {|Year|},
  month: {|Month|}
  keywords_list: [
    {|word|},
    ...
  ]
}
```

#### `top_keywords_by_day.json`
```
{
  date: {|Date|},
  keywords_list: [
    {|word|},
    ...
  ]
}
```

#### `proposals_with_keywords.json`
```
{
  id: {|Id of the proposal|},
  title: {|Title of the proposal|},
  created: {|Creation date of the proposal|},
  summary: {|Summary of the proposal|},
  keywords: [
    {
      word: {|Word in the proposal|},
      tfidf: {|TF-IDF score of the word|}
    },
    ...
  ],
  keywords_list: [
    {|Word in the proposal|},
    ...
  ]
}
```

#### `voting_info.csv`
Separator: `;`
Columns:
```
AanestysId: {|Vote ID|}
Ryhma: {|Name of the group|}
Jaa: {|Number of people in the group who voted for|}
Ei: {|Number of people in the group who voted against|}
Tyhjia: {|Number of people in the group who voted empty|}
Poissa: {|Number of people in the group who were absent|}
Yhteensa: {|Number of people in the group|}
Tyyppi: {|Type of the group (parliamentary group or opposition/government parties|}
IstuntoVPVuosi: {|Year of the vote|}
IstuntoPvm: {|Date when vote took place|}
AanestysMitatoity: {|1 if the vote has been annulled, 0 otherwise|}
KohtaKasittelyVaihe: {|Which stage the vote took place in (first/second hearing etc)|}
AanestysValtiopaivaasia: {|Id of the proposal that was voted on|}
```