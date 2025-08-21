# 📘 Cours S2 — Fichiers & chemins (stdlib)

---

## 🎯 Objectifs

- Découvrir la gestion des fichiers et dossiers en Python.
- Comparer `os.path` (héritage) et `pathlib` (moderne, orienté objet).
- Apprendre à parcourir des répertoires récursivement.
- Lire les métadonnées des fichiers (taille, extension, date de modification).
- Préparer le fil rouge : fonction `scan_dir(path)` → liste de dictionnaires.

---

## 1) Ouvrir et lire/écrire des fichiers texte

```python
# Écriture
with open("exemple.txt", "w", encoding="utf-8") as f:
    f.write("Bonjour le monde\n")

# Lecture
with open("exemple.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
print(contenu)
```

⚠️ Toujours utiliser `encoding="utf-8"` pour éviter les problèmes de caractères spéciaux.

---

## 2) `os.path` vs `pathlib`

### Avec `os.path`

```python
import os
print(os.path.basename("/tmp/test.txt"))   # "test.txt"
print(os.path.splitext("test.txt"))        # ("test", ".txt")
```

### Avec `pathlib` (recommandé)

```python
from pathlib import Path
p = Path("/tmp/test.txt")
print(p.name)     # "test.txt"
print(p.stem)     # "test"
print(p.suffix)   # ".txt"
print(p.parent)   # "/tmp"
```

👉 `pathlib` est **plus lisible** et orienté objet.

---

## 3) Lister des fichiers

### Non récursif

```python
for f in Path(".").iterdir():
    print(f)
```

### Récursif (`rglob`)

```python
for f in Path(".").rglob("*.py"):
    print(f)
```

👉 `rglob("**/*")` permet de tout lister (fichiers + dossiers).

---

## 4) Métadonnées des fichiers

```python
from pathlib import Path
from datetime import datetime

p = Path("exemple.txt")
st = p.stat()

print("Taille:", st.st_size, "octets")
print("Extension:", p.suffix)
print("Nom:", p.stem)
print("Modifié:", datetime.fromtimestamp(st.st_mtime))
```

---

## 5) Exercices pratiques

### Exo 1 — Créer un fichier et le relire

- Écrire une phrase dans `demo.txt`.
- Relire le contenu et l’afficher.

### Exo 2 — Explorer un dossier

- Demander à l’utilisateur un dossier.
- Afficher tous les fichiers `.txt` qu’il contient.

### Exo 3 — Métadonnées

- Pour chaque fichier trouvé : afficher **nom, taille, extension, date**.

---

## 6) Fil rouge — Fonction `scan_dir(path)`

Construire une fonction qui explore un dossier et renvoie une **liste de dictionnaires**.

```python
from pathlib import Path
from datetime import datetime

def scan_dir(path: str) -> list[dict]:
    out = []
    p = Path(path)
    for f in p.rglob("*"):
        if f.is_file():
            st = f.stat()
            out.append({
                "name": f.name,
                "size": st.st_size,
                "ext": f.suffix.lower(),
                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat()
            })
    return out
```

### Exemple

```python
>>> fichiers = scan_dir(".")
>>> fichiers[0]
{'name': 'cours.py', 'size': 1234, 'ext': '.py', 'mtime': '2025-08-21T09:00:00'}
```

---

## 7) Récapitulatif

- Savoir ouvrir/lire/écrire un fichier (`with open`).
- Connaître `pathlib` (préféré) et `os.path` (hérité).
- Parcourir récursivement un dossier avec `rglob()`.
- Récupérer les métadonnées essentielles (`size`, `suffix`, `stem`, `mtime`).
- Avoir un début de fonction `scan_dir(path)` → qui servira plus tard pour **indexer des documents**.
