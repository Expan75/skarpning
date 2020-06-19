# Core streamlit depends
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Misc imports
import numpy as np
import pandas as pd
import time
import urllib3
import random
from utils.helpers import capitalizeId

# data import
df = (
    pd.read_csv("data/countsPARTIES.csv", header=0, index_col="id")
    .sort_values("frånvarande", ascending=False)
    .fillna(0)
)


# Consts
PARTIES = ("KD", "SD", "S", "M", "V", "C", "L", "MP", "Partilös", "Alla")


# ------- START OF USER SELECTIONS IN SIDEBAR -------- #
# allow selection of timerange of data
time_period = st.sidebar.slider(
    label="Välj Period", min_value=0.0, max_value=100.0, value=(25.0, 75.0)
)

start_time = st.sidebar.date_input(label="Välj startdatum")
end_time = st.sidebar.date_input(label="Välj slutdatum")
# allow selection of user parties
user_parties = st.sidebar.multiselect(
    "Välj ibland partier: ", PARTIES
)  # TODO: shuffle on every list init (political bias?)

user_mp = st.sidebar.selectbox(
    "Sök på politker inom dina valda partier: %s " % ", ".join(user_parties),
    list(map(lambda x: capitalizeId(x), df.loc[df.party.isin(user_parties)].index)),
)
# ------- END OF USER SELECTIONS -------- #

# Calculate percentages of decicions
df["#beslut"] = df[["frånvarande", "ja", "nej", "avstår"]].sum(axis=1)
df["%frånvarande"] = df["frånvarande"] / df["#beslut"] * 100
df["%ja"] = df["ja"] / df["#beslut"] * 100
df["%nej"] = df["nej"] / df["#beslut"] * 100
df["%avstår"] = df["avstår"] / df["#beslut"] * 100

"""
##### NYHET: Så förändras MP närvaro under Covid-19 pandemin
# Frånvaro inom Sveriges Riksdag

Folkvalda politiker har ingen juridisk skyldighet att närvara i Riskdagen. Därmed sagt hjälper det att vara just närvarande när beslut fattas.
Data nedan visar till vilken grad riksdagsmedlemmar har röstat Ja, Nej, Avstår, eller varit frånvarande vid beslut i Riksdagen.

All data är tagen från Svenska Parlamentets Öppna Data Initiativ: https://data.riksdagen.se
"""
st.write("  \n")

# get grouped data per party
plotData = (
    df[["%frånvarande", "%ja", "%nej", "%avstår", "party"]].groupby("party").mean()
).sort_values("%frånvarande", ascending=False)

# note we skip a summary stat for "alla", hence len(PARTIES) > what we plot
fig = go.Figure(
    data=[
        go.Bar(name="Frånvarande", x=PARTIES, y=plotData["%frånvarande"]),
        go.Bar(name="Nej", x=PARTIES, y=plotData["%nej"]),
        go.Bar(name="Ja", x=PARTIES, y=plotData["%ja"]),
        go.Bar(name="Avstår", x=PARTIES, y=plotData["%avstår"]),
    ]
)

""" # Sammanfattad Frånvaro per Parti """
st.write(f"Beräknad för perioden: {start_time}-{end_time}")
fig.update_layout(
    barmode="stack",
    title_text=f"Snitt %-frånvaro för riksdagspolitiker inom varje parti vid beslut",
)
st.plotly_chart(fig, use_container_width=True)

f""" # Ledamotfrånvaro inom {user_parties} """


f"Resultat av sökning på: { user_mp }"

try:
    df.loc[user_mp.lower()]
except:
    "Finns ingen data på din valda politker..."

# TODO: add ranking in terms of % frånvaro compared to others


# TODO: dynamically load in images scraped from wikipedia (including a description)
st.image(
    "https://data.riksdagen.se/filarkiv/bilder/ledamot/5ecb17ba-ebbe-4958-a142-a5134aff9808_160.jpg"
)

