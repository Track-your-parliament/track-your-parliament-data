import pandas as pd
import xml.etree.ElementTree as ET
import time

def parse_text_from_xml(XML):
    root = ET.fromstring(XML)
    tyyppi_field = root.find("{http://www.eduskunta.fi/skeemat/siirto/2011/09/07}SiirtoMetatieto/{http://www.eduskunta.fi/skeemat/julkaisusiirtokooste/2011/12/20}JulkaisuMetatieto/*/{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiNimi")
    nimike_field = root.find("{http://www.eduskunta.fi/skeemat/siirto/2011/09/07}SiirtoMetatieto/{http://www.eduskunta.fi/skeemat/julkaisusiirtokooste/2011/12/20}JulkaisuMetatieto/*/{http://www.vn.fi/skeemat/metatietokooste/2010/04/27}Nimeke/{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}NimekeTeksti")
    sisalto_fields = root.findall("{http://www.eduskunta.fi/skeemat/siirtokooste/2011/05/17}SiirtoAsiakirja/{http://www.eduskunta.fi/skeemat/siirtokooste/2011/05/17}RakenneAsiakirja/*/{http://www.vn.fi/skeemat/asiakirjakooste/2010/04/27}SisaltoKuvaus/{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}KappaleKooste")
    
    tyyppi = ""
    if (tyyppi_field != None and tyyppi_field.text != None):
        tyyppi = tyyppi_field.text
        
    nimike =""
    if (nimike_field != None and nimike_field.text != None):
        nimike = nimike_field.text

    sisaltokuvaus = ""
    for sisalto in sisalto_fields:
        if (sisalto.text != None):
            sisaltokuvaus += (sisalto.text + "\n\n")

    return pd.Series({"tyyppi": tyyppi, "nimike": nimike, "sisaltokuvaus": sisaltokuvaus})



FILE_NAME = "./VaskiData_result.csv"

# Read the original data
df = pd.read_csv(FILE_NAME, delimiter=";", index_col=0)

# Merge new columns with parsed data to the df (function parse_text_from_xml is called for each row)
df = df.merge(df["XmlData"].apply(lambda s: parse_text_from_xml(s)), 
    left_index=True, right_index=True)

# Remove the parsed column
df.drop(columns=["XmlData"], inplace=True)

# Save file with timestamp
timestr = time.strftime("%Y%m%d_%H%M%S")
df.to_csv(f"{timestr}_xml_parsed.csv",sep=";")