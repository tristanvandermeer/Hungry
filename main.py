import downloader, linker, pretty
import time, random

def main():

    linker.crawl()

    """ oh no not yet, so many pdfs, just want length for now
    with open("file_links.txt", "r") as file:
        for url in file:
            if "math"  in url.lower(): # Only math (???)
                pretty.log(f"DOWNLOADING: {url}")
                time.sleep(random.uniform(0, 3))
                downloader.steal(url.rstrip())
        file.close()
    """


if __name__ == "__main__":
    main()