#!/usr/bin/env python3

from bs4 import BeautifulSoup

with open("test.html", "r") as f:
    list_html = f.read()

list_soup = BeautifulSoup(list_html, 'html.parser')
print(list_soup.prettify())

with open("print.html", "w") as w:
    w.write(list_html)

