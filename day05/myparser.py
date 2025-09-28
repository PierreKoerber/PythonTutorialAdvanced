import argparse

from urllib.request import urlopen
from html.parser import HTMLParser
import json
from slugify import slugify
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.title = None
        self.links = []
        self.h1 = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.in_h1 = True
        if tag == "a":
            hrefs = [v for (k, v) in attrs if k == "href"]
            self.links.extend(hrefs)
            self.links = list(set(self.links))

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1.append(data)
        if self.in_title:
            self.title = (self.title or "") + data.strip()

    def countInternalLink(self):
        counter = 0 
        for l in self.links:
            if l[0]=="/":
                counter = counter + 1
        return counter

    
def fetch_page(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        html = response.read().decode(encoding)

    parser = PageParser()
    parser.feed(html)

    #sdir = slugify(url)
    # Create Directory
    #os.makedirs(sdir)

    return {
        "h1": parser.h1,
        "url": url,
        "title": parser.title,
        "links": parser.links,
        "count_internal": parser.countInternalLink()
    }



def check_url(url: str) -> bool:
    try:
        # on envoie une requête HEAD pour limiter la charge
        req = Request(url, method="HEAD")
        with urlopen(req, timeout=5) as resp:
            code = resp.getcode()
            # considère "ok" si code 200–299
            return 200 <= code < 300
    except HTTPError as e:
        print(f"HTTP error: {e.code} for {url}")
    except URLError as e:
        print(f"Connection error: {e.reason} for {url}")
    except Exception as e:
        print(f"Other error: {e}")
    return False

