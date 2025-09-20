Super 👍 On avance dans la logique du fil rouge !
Voici un **plan structuré pour S3 — Tri, filtres, recherche**, qui s’appuie sur ce qu’on a vu en **S1 (types)** et **S2 (fichiers & chemins)**.

---

# 📘 Cours S3 — Tri, filtres, recherche

---

## 🎯 Objectifs

- Comprendre comment **filtrer** une liste de fichiers selon des critères (extension, taille, nom).
- Savoir utiliser les **motifs glob** (`glob`) et les **expressions régulières** (`re`).
- Maîtriser le tri avec `sorted()` + `key` + `reverse`.
- Appliquer ces notions au **fil rouge** : améliorer la fonction `scan_dir()` pour supporter tri et filtres.

---

## 1) Filtrer une liste en Python

Filtrer avec une **condition simple** (list comprehension) :

```python
nombres = [10, 25, 30, 5, 60]
grands = [x for x in nombres if x > 20]
print(grands)  # [25, 30, 60]
```

👉 Utile pour filtrer les fichiers par taille, extension, etc.

---

## 2) Motifs glob (`glob`)

- `*` : n’importe quelle suite de caractères.
- `?` : un seul caractère.
- `**` : sous-dossiers (si récursif).

Exemple :

```python
from pathlib import Path
for f in Path(".").glob("*.txt"):
    print(f)
```

---

## 3) Expressions régulières (`re`)

Permettent de rechercher des motifs complexes :

```python
import re

fichiers = ["rapport2025.pdf", "notes.txt", "rapport2024.doc"]
pat = re.compile(r"rapport\d+")
matches = [f for f in fichiers if pat.search(f)]
print(matches)  # ['rapport2025.pdf', 'rapport2024.doc']
```

💡 Idée : filtrer les fichiers qui contiennent un mot-clé ou un numéro.

---

## 4) Trier des fichiers

Avec `sorted()` :

```python
fichiers = [
    {"name": "a.txt", "size": 120},
    {"name": "b.txt", "size": 20}
]

# tri par taille croissante
print(sorted(fichiers, key=lambda x: x["size"]))

# tri par nom décroissant
print(sorted(fichiers, key=lambda x: x["name"], reverse=True))
```

---

## 5) Exercices pratiques

### Exo 1 — Filtrer par extension

À partir d’une liste de fichiers (résultat de `scan_dir()`), ne garder que les `.txt`.

### Exo 2 — Filtrer par taille

Ne garder que les fichiers > 1 Ko.

### Exo 3 — Regex

Trouver tous les fichiers dont le nom contient “2025”.

### Exo 4 — Tri

Trier les fichiers par date de modification (`mtime`).

---

## 6) Fil rouge — Améliorer `scan_dir()`

Ajouter des **filtres et options de tri** :

```python
import re

def filter_index(index, ext=None, min_size=None, pattern=None, sort_key="size", desc=False):
    res = index
    if ext:
        res = [x for x in res if x["ext"] == ext.lower()]
    if min_size:
        res = [x for x in res if x["size"] >= min_size]
    if pattern:
        pat = re.compile(pattern, re.IGNORECASE)
        res = [x for x in res if pat.search(x["name"])]
    return sorted(res, key=lambda x: x[sort_key], reverse=desc)
```

### Exemple

```python
index = scan_dir(".")
filtres = filter_index(index, ext=".py", min_size=100, sort_key="mtime", desc=True)

for f in filtres:
    print(f"{f['name']} ({f['size']} octets) - {f['mtime']}")
```

---

## 7) Récapitulatif

- **Filtrage** : list comprehension + conditions.
- **Glob** : motifs simples pour extensions.
- **Regex** : recherche avancée dans les noms de fichiers.
- **Tri** : `sorted()` avec `key` + `reverse`.
- **Fil rouge** : on a maintenant un **explorateur de fichiers** capable de scanner, filtrer, et trier → base d’un vrai outil d’indexation.
