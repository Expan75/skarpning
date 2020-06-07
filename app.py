import streamlit as st
import plotly.figure_factory as ff

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
import urllib3
import random

# load data
df = pd.read_csv("data/countsparties.csv", header=0, index_col="id").sort_values(
    "frånvarande", ascending=False
)

"""
##### NYHET: Så förändras MP närvaro under Covid-19 pandemin
# Frånvaro inom Sveriges Riksdag

Folkvalda politiker har ingen juridisk skyldighet att närvara i Riskdagen. Därmed sagt hjälper det att vara just närvarande när beslut fattas.
Data nedan visar till vilken grad riksdagsmedlemmar har röstat Ja, Nej, Avstår, eller varit frånvarande vid beslut i Riksdagen.

Data nedan är tagen från Svenska Parlamentets Öppna Data Initiativ: https://data.riksdagen.se/
"""


"""
# Partifrånvaro från Riksdagen
### Sök på parti:
"""
# Todo: shuffle on every init. Let's not be biased :))
parties = ("KD", "SD", "S", "M", "V", "C", "L", "MP", "Partilös", "Alla")
user_party = st.selectbox("Välj parti: ", parties)

f"Resultat av sökning på: { user_party }"

# Get party-based search results
try:
    if user_party.lower() == "partilös":
        subset = df.loc[df["party"] == "-"]
        subset
    elif user_party.lower() == "alla":
        df
    else:
        subset = df.loc[df["party"] == user_party]
        subset
except:
    "Finns ingen data på ditt valda parti..."


"""
# Ledamotfrånvaro från Riksdagen
### Sök på politker:
"""


def capitalizeId(_id):
    capNameList = list(
        map(lambda substring: substring[0].upper() + substring[1:], _id.split(" "))
    )
    return " ".join(capNameList)


# user_mp = st.text_input("Sök med namn:", "Jimmie Åkesson")

user_mp = st.selectbox(
    "Välj politker: ", list(map(lambda x: capitalizeId(x), df.index))
)

f"Resultat av sökning på: { user_mp }"

try:
    df.loc[user_mp.lower()]
except:
    "Finns ingen data på din valda politker..."
