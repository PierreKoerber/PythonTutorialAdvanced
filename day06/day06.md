# 🛡️ S6 — Robustesse & utilitaires

Jusqu’ici, notre programme marchait _quand tout se passait bien_.  
Mais que se passe-t-il si un fichier n’existe pas ? Si la page web ne répond pas ?  
Il est temps d’apprendre à **rendre notre code robuste**.

---

## 1. Gérer les erreurs avec `try/except`

En Python, les erreurs (exceptions) arrêtent le programme.  
On peut les intercepter pour réagir proprement :

```python
try:
    f = open("inexistant.txt", encoding="utf-8")
    data = f.read()
    f.close()
except FileNotFoundError:
    print("⚠️ Fichier introuvable !")
except UnicodeDecodeError:
    print("⚠️ Encodage invalide !")
```

👉 On peut attraper des exceptions spécifiques (`FileNotFoundError`, `UnicodeDecodeError`, `URLError`, etc.).

---

## 2. Exemple avec un endpoint JSON

```python
from urllib.request import urlopen
from urllib.error import URLError
import json

try:
    with urlopen("https://api.github.com/repos/python/cpython", timeout=5) as resp:
        data = resp.read().decode(resp.headers.get_content_charset() or "utf-8")
        obj = json.loads(data)
        print("Nom du repo:", obj["full_name"])
except URLError as e:
    print("⚠️ Réseau inaccessible :", e.reason)
```

---

## 3. Logging simple (sans `logging`)

Au lieu d’écrire directement avec `print`, on peut fabriquer un petit logger maison :

```python
import time

def log(msg, quiet=False):
    line = f"{time.strftime('%H:%M:%S')} | {msg}"
    if not quiet:
        print(line)

log("Ceci est un message")
```

👉 Option `quiet` permet de réduire la sortie, mais garder le log.

---

## 4. Argparse : `--quiet` et codes de sortie

Exemple de programme minimaliste :

```python
import argparse, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    try:
        print("Tout va bien")
        sys.exit(0)  # succès
    except Exception:
        sys.exit(1)  # erreur

if __name__ == "__main__":
    main()
```

👉 Convention Unix :

- `0` = succès
- `1` = échec

---

## 5. Tests rapides avec `assert`

```python
def add(a, b):
    return a + b

# test rapide
assert add(2, 3) == 5
assert add(-1, 1) == 0

print("✅ Tous les tests passent")
```

👉 `assert` sert pour des **tests unitaires rapides** (pas pour la prod).

---

## 6. Programme fil rouge (version simple)

```python
import argparse, sys, time, json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

def log(msg, quiet=False):
    line = f"{time.strftime('%H:%M:%S')} | {msg}"
    if not quiet:
        print(line)

def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Fichier introuvable: {path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError("utf-8", b"", 0, 1, f"⚠️ Encodage invalide dans {path}")

def fetch_json(url: str) -> dict:
    try:
        with urlopen(url, timeout=5) as resp:
            data = resp.read().decode(resp.headers.get_content_charset() or "utf-8")
            return json.loads(data)
    except URLError as e:
        raise URLError(f"⚠️ Impossible de contacter {url}: {e.reason}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--quiet", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_file = sub.add_parser("read-file")
    p_file.add_argument("path")

    p_web = sub.add_parser("fetch-json")
    p_web.add_argument("url")

    p_test = sub.add_parser("self-test")

    args = p.parse_args()
    try:
        if args.cmd == "read-file":
            txt = safe_read(Path(args.path))
            log(f"Lu {len(txt)} caractères", args.quiet)
            sys.exit(0)

        elif args.cmd == "fetch-json":
            obj = fetch_json(args.url)
            log(f"Clés reçues: {list(obj)[:5]}", args.quiet)
            sys.exit(0)

        elif args.cmd == "self-test":
            try:
                safe_read(Path("inexistant.txt"))
            except FileNotFoundError:
                pass
            else:
                raise AssertionError("safe_read aurait dû lever FileNotFoundError")
            log("Self-test OK ✅", args.quiet)
            sys.exit(0)

    except Exception as e:
        log(str(e), args.quiet)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

- https://jsonplaceholder.typicode.com/posts

---

## 7. Exercices

1. Modifier `safe_read` pour **retourner une valeur par défaut** (`""`) au lieu de lever une erreur.
2. Ajouter une option `--out fichier.json` dans `fetch-json` pour sauvegarder le résultat.
3. Créer un test qui vérifie que `fetch_json("http://invalid")` lève bien une `URLError`.

---

## 🎯 Fil rouge

À partir de maintenant, notre **Data Explorer** devient robuste :

- gestion des erreurs d’I/O et réseau,
- messages horodatés,
- option `--quiet` pour réduire la sortie,
- codes de sortie clairs (0/1),
- tests rapides avec `assert`.

On a désormais un outil qui **ne plante pas au premier imprévu** et informe clairement l’utilisateur.

---
