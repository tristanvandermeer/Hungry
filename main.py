import downloader, reworking_links, tester
import random
import time



def main():
    with open("compare_links.txt", "r") as file:
        for url in file:

            print(f"DOWNLOADING: {url}")
            downloader.steal(url.rstrip())

def RandomWaitTime():
    pause = random.randrange(0, 1)
    return pause

print(RandomWaitTime)