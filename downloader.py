# Wow !
import requests
import re

def steal(url):

    filename = url.split("/")[-1]  
    stripped = re.sub(r'^\d+-', '', filename) 

    response = requests.get(url)
    with open(("/Users/tristan/Exfil/OCR/Maths???/" + filename), "wb") as file:
        file.write(response.content)

#steal("https://www.ocr.org.uk/Images/677968-mark-scheme-exploring-effects-and-impact.pdf") <-- test