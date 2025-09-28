Parfait 🚀 On avance sur le **S4 — Formats de données (JSON/CSV) & stockage**, qui est une suite logique après le scan, tri et filtres.
Voici le **plan de leçon complet** avec théorie, exemples, exercices, et la partie **fil rouge**.

---

# 📘 Cours S4 — Formats de données : JSON & CSV (stdlib)

---

## 🎯 Objectifs

- Comprendre ce que sont les formats **JSON** et **CSV**.
- Savoir les **lire** et les **écrire** en Python avec la stdlib.
- Apprendre à **sauvegarder et recharger** un index de fichiers.
- Savoir **fusionner** deux index sans doublons.
- Intégrer la persistance des données au **fil rouge**.

---

## 1) JSON — JavaScript Object Notation

### Qu’est-ce que c’est ?

- Format **texte universel** pour représenter des dictionnaires et listes.
- Très utilisé pour **échanger des données** (API, fichiers de config).

### Exemple JSON

```json
[
  { "name": "rapport2025.txt", "size": 1200, "ext": ".txt" },
  { "name": "photo.png", "size": 5000, "ext": ".png" }
]
```

### En Python

```python
import json

data = {"nom": "Alex", "age": 14}
# Sauvegarde
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Lecture
with open("data.json", "r", encoding="utf-8") as f:
    d = json.load(f)
print(d["nom"])  # Alex
```

---

## 2) CSV — Comma Separated Values

### Qu’est-ce que c’est ?

- Format simple basé sur les **lignes et colonnes** (tableurs, Excel, LibreOffice).
- Chaque ligne = un enregistrement.

### Exemple CSV

```
name,size,ext
rapport2025.txt,1200,.txt
photo.png,5000,.png
```

### En Python

```python
import csv

rows = [
    {"name": "rapport2025.txt", "size": 1200, "ext": ".txt"},
    {"name": "photo.png", "size": 5000, "ext": ".png"}
]

# Écriture
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name","size","ext"])
    writer.writeheader()
    writer.writerows(rows)

# Lecture
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["size"])
```

---

## 3) Fusion d’index (éviter doublons)

👉 Stratégie : utiliser `(name, size, mtime)` comme clé unique.

```python
def merge_indexes(idx1, idx2):
    seen = {(f["name"], f["size"], f["mtime"]) for f in idx1}
    merged = idx1[:]
    for f in idx2:
        key = (f["name"], f["size"], f["mtime"])
        if key not in seen:
            merged.append(f)
            seen.add(key)
    return merged
```

---

## 4) Exercices pratiques

### Exo 1 — JSON simple

- Créer un dictionnaire `{"jeu": "Minecraft", "note": 9}`.
- Sauvegarder en JSON, puis relire et afficher la note.

### Exo 2 — CSV

- Créer une liste de jeux vidéo (nom, année, genre).
- Sauvegarder en CSV, relire et afficher seulement les noms.

### Exo 3 — Index JSON

- Scanner `samples/` avec `scan_dir()`.
- Sauvegarder l’index en JSON.
- Relire et afficher le nombre de fichiers.

### Exo 4 — Fusion

- Créer deux petits index (listes de dicts).
- Fusionner sans doublons.

---

## 5) Fil rouge — Persistance des données

Ajouter à ton projet **deux fonctions** pour sauvegarder et charger l’index.

```python
import json, csv

def export_json(index, path="index.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

def import_json(path="index.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def export_csv(index, path="index.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name","size","ext","mtime"])
        writer.writeheader()
        writer.writerows(index)
```

### Exemple d’utilisation

```python
index = scan_dir("samples")
export_json(index, "index.json")

loaded = import_json("index.json")
print("Nombre de fichiers:", len(loaded))

export_csv(loaded, "index.csv")
```

---

## 6) Récapitulatif

- **JSON** = pour les données structurées (listes/dicts).
- **CSV** = pour les données tabulaires (tableurs).
- Tu sais maintenant **sauvegarder et recharger** ton index.
- Tu as appris à **fusionner** deux index.
- Le fil rouge devient **persistant** : il garde les résultats entre deux exécutions.
