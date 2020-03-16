#!/usr/bin/env python3

import re
import sys
import time

from bs4 import BeautifulSoup
from jikanpy import Jikan


def main():
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
    len_animes = len(animes)
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
                print(" ==> MAL: " + str(mal_id) + " - " + mal_title + " - " + mal_type)
        
        #progress(count, len_animes, "Process animes list")    
        if count % 2 == 0:
            # 2 requests per second max
            time.sleep(0.3)

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    status = str(count) + '/' + str(total) + ' ' + status
    sys.stdout.write('\r[%s] %s%s ... %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

if __name__== "__main__":
      main()

