# >w<

import requests
from bs4 import BeautifulSoup

query = "site:www.ocr.org.uk filetype:pdf"
url = "https://www.google.com/search"

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {
        "q": query
    }

    response = requests.get(url, headers=headers, params=params)
    
    print(response.url)
    print(response.status_code)
    print(response.text[:1000])  # Should now contain search results HTML

except Exception as e:
    print("Error:", e)

"""
    # Optional: parse results
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'http' in href and 'pdf' in href:
            print(href)
"""




""" PDFS ARE NOT LISTED ON SITEMAP
URL = "https://www.ocr.org.uk/sitemap.xml"

url_link = requests.get(URL)
file = BeautifulSoup(url_link.text, "xml")

loc_tags = file.findAll("loc")
for tag in loc_tags:
    if (tag.text).endswith("pdf"):
        print(tag.text)
"""