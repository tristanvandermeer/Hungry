# >w<

import requests
from bs4 import BeautifulSoup

# From scratch now



""" PDFS ARE NOT LISTED ON SITEMAP
URL = "https://www.ocr.org.uk/sitemap.xml"

url_link = requests.get(URL)
file = BeautifulSoup(url_link.text, "xml")

loc_tags = file.findAll("loc")
for tag in loc_tags:
    if (tag.text).endswith("pdf"):
        print(tag.text)
"""