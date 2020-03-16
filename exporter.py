#!/usr/bin/env python3

from bs4 import BeautifulSoup
from jikanpy import Jikan
import time
import re

with open("nautilist.html", "r") as f:
    list_html = f.read()

list_soup = BeautifulSoup(list_html, 'html.parser')
animes = list_soup.find_all(class_ = 'elt')

count = 0
jikan = Jikan()

nau_types = {
    "Série TV": "tv",
    "OAV": "ova",
    "ONA": "ona",
    "Film": "movie",
    "Spécial": "special"
}

for anime in animes:
    count += 1
    
    # Nautilist
    nau_title = anime.find(class_ = 't_titre')
    nau_title = nau_title.find_all('a')
    nau_title = nau_title[0].contents[0]
    
    nau_type = anime.find(class_ = 't_type')
    nau_type = nau_type.find(class_ = 'format')
    nau_type = nau_type.contents[0]
    
    # My anime list
    search = jikan.search('anime', nau_title, parameters={'limit': '1', 'type': nau_types[nau_type]})

    if search["results"]:
        mal_id = search["results"][0]["mal_id"]
        mal_title = search["results"][0]["title"]
        mal_type = search["results"][0]["type"]
    
        if nau_title.lower() != mal_title.lower():
            print(str(count) + " - " + nau_title + " - " + nau_type, end = '')
            print(" --> MAL: " + str(mal_id) + " - " + mal_title + " - " + mal_type)

    time.sleep(0.3)
    
