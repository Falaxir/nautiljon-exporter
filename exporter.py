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
        #if count % 2 == 0:
            # 2 requests / second
            # 30 requests / minute
        time.sleep(1.5)
        progress(count, len_animes, "Process animes list")

    print('✔︎ Successfully exported!')

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    status = str(count) + '/' + str(total) + ' ' + status
    sys.stdout.write('\r[%s] %s%s ... %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def convertAnilistDataToXML(data):
    output = ''''''
    user_total_anime = 0
    user_total_watching = 0
    user_total_completed = 0
    user_total_onhold = 0
    user_total_dropped = 0
    user_total_plantowatch = 0

    for x in range(0, len(data)):
        if (data[x]['name'] == listName):
            for item in data[x]['entries']:
                s = str(item['status'])
                # print(s)
                if s == "PLANNING":
                    s = "Plan to Watch"
                    user_total_plantowatch += 1
                elif s == "DROPPED":
                    s = "Dropped"
                    user_total_dropped += 1
                elif s == "CURRENT":
                    s = "Watching"
                    user_total_watching += 1
                elif s == "PAUSED":
                    s = "On-Hold"
                    user_total_onhold += 1
                elif "completed" in s.lower():
                    s = "Completed"
                    user_total_completed += 1

                animeItem = ''
                animeItem += '    <anime>\n'
                animeItem += '        <series_animedb_id>' + str(item['media']['idMal']) + '</series_animedb_id>\n'
                animeItem += '        <series_episodes>' + str(item['media']['episodes']) + '</series_episodes>\n'
                animeItem += '        <my_watched_episodes>' + str(item['progress']) + '</my_watched_episodes>\n'
                animeItem += '        <my_score>' + str(item['score']) + '</my_score>\n'
                animeItem += '        <my_status>' + s + '</my_status>\n'
                animeItem += '    </anime>\n'
 
                output += animeItem
                user_total_anime += 1
 
 
    outputStart = '''<?xml version="1.0" encoding="UTF-8" ?>
    <!--
        Created by XML Export feature at MyAnimeList.net
        Programmed by Dranix
        Last updated 18/03/2020
    -->
 
    <myanimelist>
        <myinfo>
            <user_id>123456</user_id>
            <user_name>''' + variables['username'] + '''</user_name>
            <user_export_type>1</user_export_type>
            <user_total_anime>''' + str(user_total_anime) + '''</user_total_anime>
            <user_total_watching>''' + str(user_total_watching) + '''</user_total_watching>
            <user_total_completed>''' + str(user_total_completed) + '''</user_total_completed>
            <user_total_onhold>''' + str(user_total_onhold) + '''</user_total_onhold>
            <user_total_dropped>''' + str(user_total_dropped) + '''</user_total_dropped>
            <user_total_plantowatch>''' + str(user_total_plantowatch) + '''</user_total_plantowatch>
        </myinfo>
'''''
    output = outputStart + output + '</myanimelist>'
 
    writeToFile(output)
    


if __name__== "__main__":
      main()

