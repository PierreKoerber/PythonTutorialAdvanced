from urllib.request import urlopen
from html.parser import HTMLParser
import json

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        if tag == "a":
            hrefs = [v for (k, v) in attrs if k == "href"]
            self.links.extend(hrefs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or "") + data.strip()

def fetch_page(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        html = response.read().decode(encoding)

    parser = PageParser()
    parser.feed(html)

    return {
        "url": url,
        "title": parser.title,
        "links": parser.links
    }

# Test :
page = fetch_page("https://www.example.com/")
print(json.dumps(page, indent=2))