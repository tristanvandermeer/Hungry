import downloader
import random
import time

def RandomWaitTime():
    pause = random.uniform(0, 3) # Slow I know but I don't want to explode
    return pause

def main():
    with open("links.txt", "r") as file:
        for url in file:
            if "math"  in url.lower(): # Only math (???)
                print(f"DOWNLOADING: {url}")
                time.sleep(RandomWaitTime())
                downloader.steal(url.rstrip())


if __name__ == "__main__":
    main()