#!/usr/bin/env python3

from bs4 import BeautifulSoup

with open("nautiliste_Dranixx.html", "r") as f:
    list_html = f.read()

list_soup = BeautifulSoup(list_html, 'html.parser')

animes = list_soup.find_all(class_ = 'elt')
count = 0
for i in animes:
    title = i.find(class_ = 't_titre')
    title = title.find_all('a')
    count += 1
    print(str(count) + " " + title[0].contents[0])
    
