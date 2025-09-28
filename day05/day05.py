


from urllib.request import urlopen
import json
from html.parser import HTMLParser



def read_html(url: str) -> str:
    with urlopen(url, timeout=5) as response:
        html_bytes = response.read()  # pas .text
        encoding = response.headers.get_content_charset() or "utf-8"
        html = html_bytes.decode(encoding)
    return html




def read_json(url):

    with urlopen(url, timeout=5) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        data = response.read().decode(encoding)

    return json.loads(data)


url = "https://jsonplaceholder.typicode.com/posts"


obj = read_json(url)

for x in obj:
    print(x.get("title", "nodata")  )

  
url = "https://www.example.com/"
html = read_html(url)

print(html[:200])


# Exemple d’utilisation :
#parser = HTMLParser()
#parser.feed("<html><head><title>Demo</title></head><body><a href='/x'>link</a></body></html>")
#print(parser.title)   # Demo
#print(parser.links)   # ['/x']