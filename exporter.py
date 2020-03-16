#!/usr/bin/env python3

from bs4 import BeautifulSoup
from jikanpy import Jikan
import time
import re


def main():
    with open("test.html", "r") as f:
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
        search = jikan.search('anime', nau_title, \
                parameters={'limit': '1', 'type': nau_types[nau_type]})

        if search["results"]:
            mal_id = search["results"][0]["mal_id"]
            mal_title = search["results"][0]["title"]
            mal_type = search["results"][0]["type"]

            nau_str = re.sub("[\s:]", "", nau_title.lower())
            mal_str = re.sub("[\s:]", "", mal_title.lower())
            if nau_str != mal_str:
                print(str(count) + " - " + nau_title + " - " + nau_type, end = '')
                print(" --> MAL: " + str(mal_id) + " - " + mal_title + " - " + mal_type)

        if count % 2 == 0:
            time.sleep(0.3)


if __name__== "__main__":
      main()

