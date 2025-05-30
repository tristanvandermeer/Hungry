import downloader
import random
import time

def RandomWaitTime():
    pause = random.uniform(0, 0.9)
    return pause

def main():
    with open("compare_links.txt", "r") as file:
        for url in file:
            print(f"DOWNLOADING: {url}")
            time.sleep(RandomWaitTime())
            downloader.steal(url.rstrip())


if __name__ == "__main__":
    main()