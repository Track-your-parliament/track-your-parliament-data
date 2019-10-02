# This is an example application

import libvoikko
import numpy as np
import pandas as pd
import string
import time
import xml.etree.ElementTree as ET
from collections import defaultdict

STOP_WORDS = set([word.strip() for word in open("stop_words.txt")])
SISALTO_FIELD_PREFIX = "sisalto_level_"
voikko = libvoikko.Voikko("fi")


def parse_text_from_xml(XML):
    LEVEL = "*/"
    root = ET.fromstring(XML)
    sisalto_dict = defaultdict(str)

    # Define absolute values being interested
    paths = {
        "tyyppi": "{http://www.eduskunta.fi/skeemat/siirto/2011/09/07}SiirtoMetatieto/{http://www.eduskunta.fi/skeemat/julkaisusiirtokooste/2011/12/20}JulkaisuMetatieto/*/{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiNimi",
        "nimike": "{http://www.eduskunta.fi/skeemat/siirto/2011/09/07}SiirtoMetatieto/{http://www.eduskunta.fi/skeemat/julkaisusiirtokooste/2011/12/20}JulkaisuMetatieto/*/{http://www.vn.fi/skeemat/metatietokooste/2010/04/27}Nimeke/{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}NimekeTeksti",
    }

    # Get the values for absolutely defined paths
    for item, value in paths.items():
        field = root.find(value)
        if field is not None and isinstance(field.text, str) and len(field.text) > 0:
            sisalto_dict[item] = field.text

    summary_found = False
    # For each level get the text values and combine them together
    for levelNumber in np.arange(1, 12):
        level = LEVEL * levelNumber
        for item in root.findall(level + "{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}KappaleKooste"):
            if isinstance(item.text, str) and len(item.text) > 0:
                sisalto_dict[f"{SISALTO_FIELD_PREFIX}{levelNumber}"] += item.text + " "
                if not summary_found:
                    sisalto_dict['summary'] = item.text
                    summary_found = True

    # Return a series which has the values for absolutely defined fields and then a text value for each level that text was found
    return pd.Series(sisalto_dict)


def clean_text(text):

    # If not text return nan
    if not isinstance(text, str) or len(text) <= 0:
        return np.nan
    else:
        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))
        words = text.split()

        # Remove numbers
        words = filter(lambda x: not x.isnumeric(), words)

        # Set to lower case
        words = map(lambda x: x.lower(), words)

        # Remove stop words
        words = filter(lambda x: x not in STOP_WORDS, words)

        # Combine and return the cleaned string
        return " ".join(list(words))


def lemmatize(text):
    # If not text return nan
    if not isinstance(text, str) or len(text) <= 0:
        return np.nan
    else:
        # Get the baseform of each word using libvoikko
        words = text.split()
        words = map(lambda x: voikko.analyze(x), words)
        words = map(lambda x: x[0]["BASEFORM"] if len(x) > 0 else "", words)

        # Remove stop words
        words = filter(lambda x: x not in STOP_WORDS, words)

        # Combine and return the cleaned string
        return " ".join(list(words))


# Read the input file
df = pd.read_csv("./data/government_proposals_raw.csv", ";")

# Parse the XML column and by calling parse_text_from_xml for each row
df = df.merge(df.XmlData.apply(lambda s: parse_text_from_xml(s)), left_index=True, right_index=True)

# Drop XML
df.drop(columns=["XmlData"], inplace=True)

# Clean each text column by calling clean_text for every row on text columns
for column in df.columns:
    if SISALTO_FIELD_PREFIX in column:
        df = df.merge(
            df[column].apply(lambda s: pd.Series({f"clean_{column}": clean_text(s)})), left_index=True, right_index=True
        )
        df.drop(columns=[column], inplace=True)


# Lemmatize each text column by calling lemmatize for every row on text columns
for column in df.columns:
    if f"clean_{SISALTO_FIELD_PREFIX}" in column:
        df = df.merge(
            df[column].apply(lambda s: pd.Series({f"lemmatized_clean_{column}": lemmatize(s)})),
            left_index=True,
            right_index=True,
        )
        df.drop(columns=[column], inplace=True)

df.to_csv(f"data/government_proposals_clean.csv", sep=";")
