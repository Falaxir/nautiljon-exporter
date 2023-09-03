#!/usr/bin/env python3

import re
import requests
import sys
import time
import cloudscraper

from bs4 import BeautifulSoup
from jikanpy import Jikan

# ================================
# Please change the values below, help in the README file
# ================================

username = "CHANGE_YOUR_USERNAME"
status_list = ['vu', 'a-voir']
update_all_entries = True

# ================================

def main():
    if username == "CHANGE_YOUR_USERNAME":
        print("Please go to the file `exporter.py` and update the values according to the README file")
        exit(84)
    scraper = cloudscraper.create_scraper()
    status = 0
    data = []
    data = get_animes(status, data, scraper)
    status = 1
    data = get_animes(status, data, scraper)
    convert_to_xml(data)

def get_animes(status, data, scraper):
    url = ("https://www.nautiljon.com/membre/"
            f"{status_list[status]},{username},anime.html")
    page = scraper.get(url)
    list_soup = BeautifulSoup(page.text, 'html.parser')
    animes = list_soup.find_all(class_ = 'elt')

    count = 0
    jikan = Jikan()
    nau_types = {
            "Série TV": "tv",
            "OAV": "ova",
            "ONA": "ona",
            "Film": "movie",
            "Spécial": "special",
            "Court-métrage": "movie",
            "Inconnu": "tv",
            }
    len_animes = len(animes)
    f = open("mismatch.log", 'a+')

    for anime in animes:
        count += 1

        # Process on the Nautilist
        nau_title = anime.find(class_ = 't_titre')
        nau_title = nau_title.find_all('a')
        nau_title = nau_title[0].contents[0]

        nau_type = anime.find(class_ = 't_type')
        nau_type = nau_type.find(class_ = 'format')
        nau_type = nau_type.contents[0]

        # TODO: Support "Abandonné" (Dropped), "En pause" (On Hold)
        if status: # 1 
            nau_status = 'P'  # Plan to Watch
            nau_ep = '0'
            nau_score = '0'
        else:      # 0
            nau_status = 'C'  # Completed
            
            nau_ep = anime.find(class_ = 't_progression')
            nau_ep = nau_ep.contents[1]

            nau_ep = nau_ep.split(' /')[0].strip()
            
            nau_score = anime.find(class_ = 't_note')
            nau_score = nau_score.find(class_ = 'note_val')
            nau_score = nau_score.contents[0]

        # Search of MAL ID
        search = jikan.search('anime', nau_title, \
                parameters={'limit': '1', 'type': nau_types[nau_type]})

        if search["data"]:
            mal_id = search["data"][0]["mal_id"]
            mal_title = search["data"][0]["title"]
            mal_type = search["data"][0]["type"]

            nau_str = re.sub("[\s:-]", "", nau_title.lower())
            mal_str = re.sub("[\s:-]", "", mal_title.lower())

            if nau_str != mal_str or nau_types[nau_type] != mal_type.lower():
                f.write(str(count) + " - " + nau_title + " - " + nau_type)
                f.write(" ==> MAL: " + str(mal_id) + " - " + mal_title + " - " + mal_type + '\n')
        
        data.append({"title": nau_title, "id": mal_id, "status": nau_status, 
            "progress": nau_ep, "score": nau_score})

        # 2 requests / second
        # 30 requests / minute
        time.sleep(2)
        progress(count, len_animes, "Process animes list")

    print('✔︎ Successfully exported!')
    return data

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    status = str(count) + '/' + str(total) + ' ' + status
    sys.stdout.write('\r[%s] %s%s ... %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def convert_to_xml(data):
    output = ''''''
    user_total_anime = 0
    user_total_completed = 0
    user_total_plantowatch = 0

    for item in data:
        s = item['status']
        if s == 'C':
            s = "Completed"
            user_total_completed += 1
        elif s == 'P':
            s = "Plan to Watch"
            user_total_plantowatch += 1

        anime_item = ''
        anime_item += '    <anime>\n'
        anime_item += '        <series_animedb_id>' + str(item['id']) + '</series_animedb_id>\n'
        anime_item += '        <series_title><![CDATA[' + item['title'] + ']]></series_title>\n'
        anime_item += '        <my_watched_episodes>' + item['progress'] + '</my_watched_episodes>\n'
        anime_item += '        <my_score>' + item['score'] + '</my_score>\n'
        anime_item += '        <my_status>' + s + '</my_status>\n'
        anime_item += '        <update_on_import>1</update_on_import>\n' if update_all_entries else '        <update_on_import>0</update_on_import>\n'
        anime_item += '    </anime>\n'

        output += anime_item
        user_total_anime += 1


    output_start = '''\
<?xml version="1.0" encoding="UTF-8" ?>
<!--
    Created by XML Export feature at MyAnimeList.net
    Programmed by Dranix
    Last updated 18/03/2020
-->

<myanimelist>
    <myinfo>
        <user_id></user_id>
        <user_name>''' + username + '''</user_name>
        <user_export_type>1</user_export_type>
        <user_total_anime>''' + str(user_total_anime) + '''</user_total_anime>
        <user_total_watching>0</user_total_watching>
        <user_total_completed>''' + str(user_total_completed) + '''</user_total_completed>
        <user_total_onhold>0</user_total_onhold>
        <user_total_dropped>0</user_total_dropped>
        <user_total_plantowatch>''' + str(user_total_plantowatch) + '''</user_total_plantowatch>
    </myinfo>
'''
    output = output_start + output + '</myanimelist>'
    
    f = open("nautilist.xml", 'w')
    f.write(output)
    f.close()
    
    print('✔︎ Successfully converted!')



if __name__== "__main__":
    main()

