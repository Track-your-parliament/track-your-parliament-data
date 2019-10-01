# track-your-parliament-data

Data for project Track-your-parliament

Data has been fetched and parsed from https://avoindata.eduskunta.fi and it's using "CC Nimeä 4.0" -license (*"Data on tarjolla palvelussa JHS 189 -suosituksen mukaisesti CC Nimeä 4.0 -lisenssillä"*)

`stop_words.txt` -file has been gathered from below sources:
- https://github.com/stopwords-iso/stopwords-fi
- https://github.com/Alir3z4/stop-words

### Data models

#### `voting_info.json`

#### `proposals_with_keywords`

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
  Votes: [
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
  Year: {|Year|},
  Tags: [
    {|word|},
    ...
  ]
}
```

#### `top_keywords_by_month.json`
```
{
  Year: {|Year|},
  Month: {|Month|}
  Tags: [
    {|word|},
    ...
  ]
}
```