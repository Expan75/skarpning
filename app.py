import streamlit as st
import plotly.figure_factory as ff

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
import urllib3
import random

# TODO: add time range as a filter. Should be applied before everything else (i.e. before transformation logic to raw)


# load data
df = (
    pd.read_csv("data/countsparties.csv", header=0, index_col="id")
    .sort_values("frånvarande", ascending=False)
    .fillna(0)
)
# Calculate percentages of decicions
df["#beslut"] = df[["frånvarande", "ja", "nej", "avstår"]].sum(axis=1)
df["%frånvarande"] = df["frånvarande"] / df["#beslut"]
df["%ja"] = df["ja"] / df["#beslut"]
df["%nej"] = df["nej"] / df["#beslut"]
df["%avstår"] = df["avstår"] / df["#beslut"]

"""
##### NYHET: Så förändras MP närvaro under Covid-19 pandemin
# Frånvaro inom Sveriges Riksdag

Folkvalda politiker har ingen juridisk skyldighet att närvara i Riskdagen. Därmed sagt hjälper det att vara just närvarande när beslut fattas.
Data nedan visar till vilken grad riksdagsmedlemmar har röstat Ja, Nej, Avstår, eller varit frånvarande vid beslut i Riksdagen.

Data nedan är tagen från Svenska Parlamentets Öppna Data Initiativ: https://data.riksdagen.se
"""

plotData = (
    df[["%frånvarande", "%ja", "%nej", "%avstår", "party"]].groupby("party").mean()
).sort_values("%frånvarande", ascending=False)
# plotData

import plotly.graph_objects as go

parties = ("KD", "SD", "S", "M", "V", "C", "L", "MP", "Partilös", "Alla")

# note we skip a summary stat for "alla", hence len(parties) > what we plot
fig = go.Figure(
    data=[
        go.Bar(name="Frånvarande", x=parties, y=plotData["%frånvarande"]),
        go.Bar(name="Ja", x=parties, y=plotData["%ja"]),
        go.Bar(name="Nej", x=parties, y=plotData["%nej"]),
        go.Bar(name="Avstår", x=parties, y=plotData["%avstår"]),
    ]
)
# Change the bar mode
fig.update_layout(
    barmode="stack", title_text="Snitt frånvaro (%) per Parti under perioden 2019-2020"
)
st.plotly_chart(fig, use_container_width=True)


"""
# Partifrånvaro från Riksdagen
### Sök på parti:
"""
# TODO: shuffle on every init. Let's not be biased :))
user_party = st.selectbox("Välj parti: ", parties)

f"Resultat av sökning på: { user_party }"

# TODO: results should be primarily a graphed representation of averaged percentages
# Get party-based search results
try:
    if user_party.lower() == "partilös":
        subset = df.loc[df["party"] == "-"]
    elif user_party.lower() == "alla":
        subset = df
    else:
        subset = df.loc[df["party"] == user_party]
except:
    "Finns ingen data på ditt valda parti..."

# Graph the relevant data

# top 5 frånvaro but only %tages
st.table(subset[["%frånvarande", "%ja", "%nej", "%avstår"]][0:10])


f""" # Ledamotfrånvaro från Riksdagen 
### Sök på politker inom {user_party}:
# """


def capitalizeId(_id):
    capNameList = list(
        map(lambda substring: substring[0].upper() + substring[1:], _id.split(" "))
    )
    return " ".join(capNameList)


user_mp = st.selectbox(
    "Välj politker: ",
    list(map(lambda x: capitalizeId(x), df.loc[df.party == user_party].index)),
)

f"Resultat av sökning på: { user_mp }"

try:
    df.loc[user_mp.lower()]
except:
    "Finns ingen data på din valda politker..."

# TODO: add ranking in terms of % frånvaro compared to others

st.write(
    '<img src="https://data.riksdagen.se/filarkiv/bilder/ledamot/5ecb17ba-ebbe-4958-a142-a5134aff9808_160.jpg/>'
)
