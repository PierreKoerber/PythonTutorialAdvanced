
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        if tag == "a":
            for (attr, value) in attrs:
                if attr == "href":
                    self.links.append(value)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or "") + data.strip()


# Exemple d’utilisation :
parser = MyHTMLParser()
parser.feed("<html><head><title>Demo</title></head><body><a href='/x'>link</a></body></html>")
print(parser.title)   # Demo
print(parser.links)   # ['/x']