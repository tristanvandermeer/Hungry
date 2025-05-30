# >w<

import requests
from bs4 import BeautifulSoup
import os
from serpapi import GoogleSearch

query = "site:www.ocr.org.uk filetype:pdf"
url = "https://www.google.com/search"

# Serpapi key
with open("/Users/tristan/Secrets/impostor.txt", "r") as file:
    api_key = file.readline()

params = {
    "engine": "google",
    "q": "site:www.ocr.org.uk filetype:pdf",
    "api_key": api_key,
    "num" : "100",
    "start" : 0
}

# No repeats
all_links = set()

while True:
    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get("organic_results", [])
    if not organic_results:
        break

    for result in organic_results:
        link = result.get("link", "")
        if link.endswith(".pdf"):
            all_links.add(link)

    # Next page
    params["start"] += 100


with open("links.txt", "w") as link_file:
    for link in all_links:
        link_file.write(link + "\n")

"""
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