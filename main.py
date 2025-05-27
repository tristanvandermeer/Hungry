# >w<

import requests
from bs4 import BeautifulSoup

# From scratch now
query = "site:www.ocr.org.uk filetype:pdf"
url = "https://html.duckduckgo.com/html/"

try:
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {
        "q" : query
    }
    response = requests.post(url, headers=headers, data=data)
    
    print(response.url)
    print(response.status_code)
    print(response.text[:1000])  # See what's actually returned

except(Exception):
    print("Balls")


""" PDFS ARE NOT LISTED ON SITEMAP
URL = "https://www.ocr.org.uk/sitemap.xml"

url_link = requests.get(URL)
file = BeautifulSoup(url_link.text, "xml")

loc_tags = file.findAll("loc")
for tag in loc_tags:
    if (tag.text).endswith("pdf"):
        print(tag.text)
"""