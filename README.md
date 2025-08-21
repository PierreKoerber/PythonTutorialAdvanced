# 🎯 Fil rouge

## “Data Explorer” — un outil en ligne de commande qui :

- **Parcourt** un dossier (récursif), **indexe** les fichiers (nom, taille, extension, date).
- **Trie/filtre** (par taille, extension, date, motif).
- **Recherche** par motif (glob/regex).
- **Lit une URL**, **parse** quelques infos (titres/liens), et **stocke** en JSON/CSV.
- **Exporte** l’index (JSON/CSV), **importe**/fusionne.
- 100% stdlib : `os`, `pathlib`, `sys`, `argparse`, `glob`, `re`, `csv`, `json`, `datetime`, `urllib.request`, `html.parser`, `shutil`.

Livrable final : un script `data_explorer.py` + un dossier `samples/` et un `README.md` avec exemples d’utilisation.

---

# 🗓️ Plan sur 8 semaines

## S1 — Types & opérations de base (révision profonde) : (./day01/day01.md)

- **Objets fondamentaux** : `str`, `list`, `dict`, `set`, `tuple`
- Méthodes clés (strings, listes), slicing, `sorted()`, `key=`, `reverse=`
- **Exos** : top N mots d’une phrase (split/count/sorted)
- **Fil rouge** : prototype d’**index** (liste de dicts) et tri simple :

  ```python
  files = [{"name":"a.txt","size":120}, {"name":"b.pdf","size":20}]
  print(sorted(files, key=lambda x: x["size"], reverse=True))
  ```

## S2 — Fichiers & chemins (stdlib)

- `pathlib` (recommandé) vs `os.path`; encodage `utf-8`
- Lister, **récursion** : `Path.rglob("**/*")`
- Métadonnées : `.stat().st_size`, `.suffix`, `.stem`, `datetime.fromtimestamp`
- **Fil rouge** : fonction `scan_dir(path)->list[dict]` (name, size, ext, mtime).

## S3 — Tri, filtres, recherche

- `glob` (motifs), `re` (regex, `re.search`)
- Filtres composés (extension, taille min/max, date après)
- **Argparse (base)** : `--path`, `--ext`, `--min-size`, `--pattern`
- **Fil rouge** : `filter_index(index, args)` + `sorted(index, key=...)`

## S4 — Formats de données (JSON/CSV) & stockage

- `json.dump/load`, `csv.writer/DictWriter`, `newline=""`
- **Fusion** d’index (éviter doublons via (path, size, mtime))
- **Argparse** : `--export-json`, `--export-csv`, `--import-json`
- **Fil rouge** : persister l’index et recharger au démarrage.

## S5 — Réseau : lire des URL & parser HTML (stdlib)

- `urllib.request.urlopen`, timeouts, encodage
- **html.parser** minimal : extraire `<title>`, `<a href>`
- **Argparse** : `--fetch-url URL --out page.json`
- **Fil rouge** : stocker `{url, title, links:[...]}` en JSON.

## S6 — Robustesse & utilitaires

- `try/except`, `FileNotFoundError`, `UnicodeDecodeError`, `URLError`
- **Logging simple** (écrire lignes horodatées) sans `logging` pour rester simple
- **Argparse** : `--quiet`, codes de sortie (`sys.exit(0/1)`)
- **Fil rouge** : sécuriser I/O, messages clairs, tests rapides (assert).

## S7 — Regroupements & statistiques (bonus stdlib)

- `collections.Counter`, `defaultdict`, `itertools.groupby`
- Stats de l’index : nb fichiers par extension, taille totale, top 5 plus gros
- **Argparse** : `--stats` (imprime un résumé)
- **Fil rouge** : générer un petit **rapport texte**.

## S8 — Gel du livrable & démo finale

- Nettoyage : aide CLI `-h`, exemples dans README, structure du projet
- Scénario de démo (3 min) + dataset `samples/`
- **Livrable** : `data_explorer.py`, `README.md`, `samples/`, exports JSON/CSV

---

# 🧩 Squelettes prêts à coller (extraits)

## 1) Scan & lignes de commande

```python
# data_explorer.py
from pathlib import Path
from datetime import datetime
import argparse, json, csv, sys, re
from urllib.request import urlopen

def scan_dir(path: str) -> list[dict]:
    p = Path(path)
    out = []
    for f in p.rglob("*"):
        if f.is_file():
            st = f.stat()
            out.append({
                "path": str(f),
                "name": f.name,
                "ext": f.suffix.lower(),
                "size": st.st_size,
                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            })
    return out

def build_parser():
    p = argparse.ArgumentParser(description="Data Explorer (stdlib only)")
    p.add_argument("--path", default=".", help="Dossier de départ")
    p.add_argument("--ext", help="Filtrer par extension (.txt)")
    p.add_argument("--pattern", help="Regex sur le nom de fichier")
    p.add_argument("--min-size", type=int, help="Taille min en octets")
    p.add_argument("--sort", choices=["name","size","ext","mtime"], default="size")
    p.add_argument("--desc", action="store_true", help="Tri décroissant")
    p.add_argument("--export-json")
    p.add_argument("--export-csv")
    p.add_argument("--import-json")
    p.add_argument("--fetch-url")
    p.add_argument("--out")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--quiet", action="store_true")
    return p
```

## 2) Filtres & tri

```python
def apply_filters(index, args):
    res = index
    if args.ext:
        res = [x for x in res if x["ext"] == args.ext.lower()]
    if args.pattern:
        pat = re.compile(args.pattern, re.IGNORECASE)
        res = [x for x in res if pat.search(x["name"])]
    if args.min_size:
        res = [x for x in res if x["size"] >= args.min_size]
    return sorted(res, key=lambda x: x[args.sort], reverse=args.desc)
```

## 3) Export/Import

```python
def export_json(rows, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

def export_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path","name","ext","size","mtime"])
        w.writeheader(); w.writerows(rows)

def import_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
```

## 4) Fetch URL & parse HTML (titre + liens)

```python
from html.parser import HTMLParser

class SimpleHTML(HTMLParser):
    def __init__(self): super().__init__(); self.title=""; self._in_title=False; self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag=="title": self._in_title=True
        if tag=="a":
            for k,v in attrs:
                if k=="href": self.links.append(v)
    def handle_endtag(self, tag):
        if tag=="title": self._in_title=False
    def handle_data(self, data):
        if self._in_title: self.title += data.strip()

def fetch_url(url: str) -> dict:
    with urlopen(url, timeout=10) as r:
        data = r.read()
        html = data.decode("utf-8", errors="replace")
    p = SimpleHTML(); p.feed(html)
    return {"url": url, "title": p.title, "links": p.links}
```

## 5) Stats rapides

```python
from collections import Counter
def stats(index):
    c = Counter(x["ext"] for x in index)
    total = sum(x["size"] for x in index)
    top = sorted(index, key=lambda x: x["size"], reverse=True)[:5]
    return {"count": len(index), "total_bytes": total, "by_ext": c.most_common(), "top5": top}
```

---

# ✅ Travail de fin de cycle

- **Script unique** `data_explorer.py` avec aide CLI complète (`-h`)
- **Démo** sur un dossier `samples/` + une URL publique (extraction `title`/`href`)
- **Exports** `index.json`, `index.csv`, `page.json`
- **README** avec 5 commandes d’exemple et captures de sorties
