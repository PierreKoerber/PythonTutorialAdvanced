Voici une proposition de leçon complète pour **S5 — Réseau : lire des URL & parser HTML (stdlib)**.
J’ai gardé le style des semaines précédentes : intro théorique, exemples concrets, puis exercices et fil rouge.

---

# 📡 S5 — Réseau : lire des URL & parser HTML (stdlib)

Jusqu’ici, tu as travaillé sur des fichiers locaux. Cette fois-ci, on passe au **web** : lire des pages et en extraire de l’information. Pas besoin de bibliothèques externes comme `requests` ou `BeautifulSoup` — on reste dans la **stdlib** de Python.

---

## 1. Lire une page web

On utilise `urllib.request` :

```python
from urllib.request import urlopen

url = "https://www.example.com/"
with urlopen(url, timeout=5) as response:
    html_bytes = response.read()  # contenu brut
    encoding = response.headers.get_content_charset() or "utf-8"
    html = html_bytes.decode(encoding)

print(html[:200])  # affiche les 200 premiers caractères
```

👉 Points clés :

- `timeout=5` évite que le programme reste bloqué.
- Le contenu est en **bytes**, il faut décoder (`decode`) selon l’encodage annoncé dans l’en-tête HTTP.
- Si rien n’est annoncé : utiliser `"utf-8"` par défaut.

---

## 2. Parser du HTML minimaliste

Python propose un parseur très simple : `html.parser`. On peut définir une sous-classe de `HTMLParser` pour réagir quand on rencontre certaines balises :

```python
from html.parser import HTMLParser

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
```

---

## 3. Mettre ensemble : URL → titre + liens

```python
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
```

---

## 4. Ligne de commande avec argparse

On ajoute une petite CLI pour faire ça en direct :

```python
import argparse

def main():
    p = argparse.ArgumentParser(description="Fetch a web page and extract links")
    p.add_argument("--fetch-url", required=True, help="URL de la page à analyser")
    p.add_argument("--out", default="page.json", help="Fichier de sortie JSON")
    args = p.parse_args()

    data = fetch_page(args.fetch_url)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Résultats sauvegardés dans {args.out}")

if __name__ == "__main__":
    main()
```

👉 Exemple d’exécution :

```bash
python data_explorer.py --fetch-url https://www.python.org --out python.json
```

---

## 5. Exercices

1. Modifier le parseur pour aussi extraire les balises `<h1>`.
2. Compter le nombre de liens internes (`href` commençant par `/`) vs externes (`http…`).
3. Faire un petit crawler à 1 niveau : télécharger une page, puis télécharger toutes les pages internes liées depuis elle (attention à ne pas aller trop loin !).

---

## 🎯 Fil rouge

Le programme doit pouvoir :

- Lire une URL donnée (`--fetch-url`).
- Extraire le `title` et la liste des `href`.
- Sauvegarder dans un JSON de la forme :

```json
{
  "url": "https://www.example.com/",
  "title": "Example Domain",
  "links": ["https://www.iana.org/domains/example"]
}
```
