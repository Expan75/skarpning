from bs4 import BeautifulSoup

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
import urllib3

df = pd.read_csv("data/wiki_profiles.csv", index_col="id")
print(df.head())

example_url = df.full_url[0]

http = urllib3.PoolManager()
res = http.request("GET", example_url)
soup = BeautifulSoup(res.data, "html.parser")

imgLink = soup.find("a", class_="image")["href"]

print(imgLink)


def extractProfileData(profile_soup):
    return


"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Text-x-generic_with_pencil-2.svg/84px-Text-x-generic_with_pencil-2.svg.png"
