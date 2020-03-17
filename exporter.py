#!/usr/bin/env python3

import re
import requests
import sys
import time

from bs4 import BeautifulSoup
from jikanpy import Jikan

def main():
    username = "dranixx"
    status = 0
    status_list = ['vu', 'a-voir']
    url = ("https://www.nautiljon.com/membre/"
          f"{status_list[status]},{username},anime.html")
    get_animes(status, url)

def get_animes(status, url):
    page = requests.get(url)    
    list_soup = BeautifulSoup(page.text, 'html.parser')
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

        # Process on the Nautilist
        nau_title = anime.find(class_ = 't_titre')
        nau_title = nau_title.find_all('a')
        nau_title = nau_title[0].contents[0]

        nau_type = anime.find(class_ = 't_type')
        nau_type = nau_type.find(class_ = 'format')
        nau_type = nau_type.contents[0]

        nau_ep = anime.find(class_ = 'ep_prog')

        nau_status = anime.find(class_ = 't_status')

        # Search of MAL ID
        search = jikan.search('anime', nau_title, \
                parameters={'limit': '1', 'type': nau_types[nau_type]})

        if search["results"]:
            mal_id = search["results"][0]["mal_id"]
            mal_title = search["results"][0]["title"]
            mal_type = search["results"][0]["type"]
            
            nau_str = re.sub("[\s:-]", "", nau_title.lower())
            mal_str = re.sub("[\s:-]", "", mal_title.lower())
            if nau_str != mal_str or nau_types[nau_type] != mal_type.lower():
                print(str(count) + " - " + nau_title + " - " + nau_type, end = '')
                print(" ==> MAL: " + str(mal_id) + " - " + mal_title + " - " + mal_type)
        
        #progress(count, len_animes, "Process animes list")    
        if count % 2 == 0:
            # 2 requests per second max
            time.sleep(0.4)

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

