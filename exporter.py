#!/usr/bin/env python3

from bs4 import BeautifulSoup
from jikanpy import Jikan

with open("nautilist.html", "r") as f:
    list_html = f.read()

list_soup = BeautifulSoup(list_html, 'html.parser')
animes = list_soup.find_all(class_ = 'elt')

count = 0
jikan = Jikan()

naut_type = {
    "Série TV": "TV",
    "OAV": "OVA",

}

for anime in animes:
    count += 1
    
    title = anime.find(class_ = 't_titre')
    title = title.find_all('a')
    title = title[0].contents[0]
    print(str(count) + " - " + title)
    
    search = jikan.search('anime', title, parameters={'limit':'1'})
    mal_id = search["results"][0]["mal_id"]
    mal_title = search["results"][0]["title"]
    print(str(mal_id) + " - " + mal_title)
    
