import urllib3
from bs4 import BeautifulSoup
import pandas as pd

# Generate profile list from MPs (req from Wikipedia)
mps_wiki = (
    "https://en.wikipedia.org/wiki/List_of_members_of_the_Riksdag,_2018%E2%80%932022"
)

http = urllib3.PoolManager()
res = http.request("GET", mps_wiki)
soup = BeautifulSoup(res.data, "html.parser")


def extractData(td):
    try:
        anchor = td.find("a")
        name = anchor["title"]
        url = anchor["href"]
    except:
        print("skipping irrelevant td...")
        return
    return name, url


# Generate dict mp_name : url_to_wiki_profile
rows = soup.find("table", class_="sortable").find_all("tr")[1:]
data = {"name": [], "url": []}
for row in rows:
    name, url = extractData(row.find_all("td")[2:3][0])
    data["name"].append(name.lower())
    data["url"].append(url)

# example clean data: ("åsa lindestam", "https://sv.wikipedia.org/wiki/%C3%85sa_Lindestam")
df = pd.DataFrame(data)
print(df.head())

BASE_URL = "https://se.wikipedia.org"

# open MPs profiles df
def formatFullWikiUrl(partial):
    return BASE_URL + partial


fullUrls = list(map(lambda url: formatFullWikiUrl(url), df.url.tolist()))

df.insert(2, "full_url", fullUrls)

df.to_csv("data/wiki_profiles.csv")
