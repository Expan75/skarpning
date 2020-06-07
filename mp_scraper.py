# Script for scraping image links per MP and neatly dumping them
BASE_URL = "https://www.riksdagen.se"
MP_SUBDOMAIN = "/en/members-and-parties/#parties"

from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# setup connection and request
http = urllib3.PoolManager()
res = http.request("GET", BASE_URL + MP_SUBDOMAIN)
soup = BeautifulSoup(res.data, "html.parser")

mpContainers = soup.find_all("a", class_="fellow-item-container")
# print(mpContainers[0])


# imgSources = [container.find("img")["data-src"] for container in mpContainers]
# print(imgSources[0])
def extractContainerInfo(container):
    imgContainer = container.find("img")
    src = imgContainer["data-src"]
    rawInfo = imgContainer["alt"].split("(")
    name = rawInfo[0]
    party = rawInfo[1][:-1]

    return name, party, src


extractedInfo = [extractContainerInfo(container) for container in mpContainers]
# print(extractedInfo[0:3])


# setup new df and ready export
columns = ["name", "party", "src"]
df = pd.DataFrame(data=extractedInfo, columns=columns)
# print(df.party.unique())

# before we do so, let's clean up the english party names and replace them with standard swedish aliases
aliases = {
    "Lib": "L",
    "ChrDem": "KD",
    "SocDem": "S",
    "Cen": "C",
    "Grn": "MP",
    "Mod": "M",
    "SweDem": "SD",
    "Lft": "V",
}

# helper function to do just that
def aliasReplacer(partyString):
    try:
        return aliases[partyString]
    except KeyError:
        return "-"


df.party = df.party.apply(lambda x: aliasReplacer(x))
print(df.head())

df.to_csv("data/imgLinks.csv")
