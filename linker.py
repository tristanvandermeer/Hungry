# Previous crawl didn't work, wget does a better job so here we go again

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import time
import random
from collections import deque
import http.client

start_url = "https://www.ocr.org.uk"
domain = "www.ocr.org.uk"
visited = set()
pdf_links = set()
pedophile = open("pdf_links.txt", "w")

user_agents = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.80",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
               "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
               "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

def is_internal(url):
    return urlparse(url).netloc == domain or urlparse(url).netloc == ''

def normalize_url(url):
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    normalized = parsed._replace(query="", fragment="").geturl()
    return normalized.rstrip('/')

def crawl(start_url, max_depth=6):
    queue = deque()
    queue.append((start_url, 0))
    
    while queue:
        current_url, depth = queue.popleft()

        normalized_url = normalize_url(current_url)
        if normalized_url in visited or depth > max_depth:
            continue
        visited.add(normalized_url)

        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            print(f"[{depth}] Crawling: {current_url}")
            response = requests.get(current_url, timeout=10, headers=headers)
            time.sleep(random.uniform(0, 0.8))  # i love humans !

            if response.status_code != 200:
                if response.status_code in [403, 429]:
                    wait_time = random.randint(30, 60)
                    print(f"  -> Rate-limited. Waiting {wait_time}s.")
                    time.sleep(wait_time)
                else:
                    print(f"  -> Skipped (status {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                link = urljoin(current_url, a_tag['href'])

                if link.startswith(("mailto:", "tel:", "javascript:")): # i miss the rage
                    continue
                
                if not is_internal(link):
                    continue

                link = normalize_url(link)

                if link.lower().endswith('.pdf'):
                    if link not in pdf_links:
                        print(f"Found PDF: {link}")
                        pedophile.write(link + "\n")
                        pedophile.flush()
                elif link not in visited:
                    queue.append((link, depth + 1))

        except (requests.exceptions.ConnectionError, http.client.RemoteDisconnected) as e:
            print(f"  !! Connection issue: {e}")
            print("  -> Waiting 10s before retrying...")
            time.sleep(10)
            queue.appendleft((current_url, depth))

        except Exception as e:
            print(f"  !! Error: {e}")

crawl(start_url)
pedophile.close()

"""
with open("found_pdfs.txt", "w") as file:
    for pdf in sorted(pdf_links):
        file.write(pdf + "\n")
    file.close()
"""
print("\nTotal PDFs found:", len(pdf_links))
