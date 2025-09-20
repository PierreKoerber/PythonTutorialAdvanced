Super 👍 tu as raison : les **expressions régulières (regex)** méritent une explication claire et progressive, surtout si ton fils n’en a jamais vu.

Voici une **mini-leçon complète** à intégrer au **S3 — Tri, filtres, recherche**, avec exemples adaptés au fil rouge (recherche de fichiers).

---

# 📘 Expressions régulières (`re`)

---

## 🎯 Objectif

Apprendre à utiliser les **regex** pour rechercher des motifs (patterns) dans du texte ou des noms de fichiers.

---

## 1) Qu’est-ce qu’une regex ?

- Une **expression régulière** = une **phrase spéciale** pour décrire un motif de texte.
- Utilisée partout : recherche de fichiers, validation d’email, recherche de mots dans un texte.
- En Python : via le module `re`.

👉 Exemple simple :

```python
import re
motif = re.compile("chat")
print(bool(motif.search("le chat dort")))  # True
print(bool(motif.search("chien")))         # False
```

---

## 2) Les symboles les plus utiles

### 🔤 Caractères simples

- `"chat"` → cherche exactement le mot "chat"
- `"2025"` → cherche 2025

### 🎭 Joker

- `"."` → n’importe quel caractère

  - `a.c` trouve `abc`, `axc`, `a-c`

### 🔢 Quantificateurs

- `*` → 0 ou plusieurs fois
- `+` → au moins une fois
- `?` → 0 ou 1 fois

Exemples :

- `ab*` trouve `a`, `ab`, `abb`, `abbbbb`
- `ab+` trouve `ab`, `abb`, `abbbb` (mais pas `a`)
- `colou?r` trouve `color` et `colour`

### ⛓️ Classes de caractères

- `[abc]` → un caractère parmi a, b, ou c
- `[0-9]` → un chiffre
- `[a-z]` → une lettre minuscule
- `[A-Za-z]` → lettre majuscule ou minuscule

Exemple :

- `rapport[0-9]` → `rapport1`, `rapport2`…
- `rapport[0-9]{4}` → `rapport2025`

### 🎯 Ancres

- `^` → début de ligne
- `$` → fin de ligne

Exemple :

- `^plan` → commence par “plan”
- `\.txt$` → finit par “.txt”

(`\.` car `.` est spécial, donc on échappe avec `\`)

---

## 3) Exemple sur des fichiers

```python
import re

fichiers = ["rapport2025.pdf", "plan2024.txt", "photo.png", "notes2025.txt"]

# tous les fichiers avec "2025"
pat = re.compile(r"2025")
print([f for f in fichiers if pat.search(f)])
# ['rapport2025.pdf', 'notes2025.txt']

# tous les fichiers qui finissent par .txt
pat = re.compile(r"\.txt$")
print([f for f in fichiers if pat.search(f)])
# ['plan2024.txt', 'notes2025.txt']

# rapport + année sur 4 chiffres
pat = re.compile(r"rapport\d{4}")
print([f for f in fichiers if pat.search(f)])
# ['rapport2025.pdf']
```

---

## 4) Intégration dans le fil rouge

Dans la fonction `filter_index()` :

```python
import re

def filter_index(index, pattern=None):
    res = index
    if pattern:
        pat = re.compile(pattern, re.IGNORECASE)
        res = [x for x in res if pat.search(x["name"])]
    return res
```

### Exemple d’utilisation

```python
index = scan_dir("samples")

# Tous les fichiers avec 2025 dans le nom
res = filter_index(index, pattern="2025")

# Tous les fichiers finissant par .txt
res = filter_index(index, pattern=r"\.txt$")
```

---

## 5) Exercices pratiques

1. Trouver tous les fichiers qui commencent par `rapport`.
2. Trouver tous les fichiers qui contiennent une année (quatre chiffres).
3. Trouver tous les fichiers dont l’extension est `.png` ou `.jpg`.
4. Bonus : Trouver les fichiers qui contiennent le mot “plan” **ou** “notes”.

---

## 6) Résumé à retenir

- `.` = n’importe quel caractère
- `*`, `+`, `?` = répétitions
- `[0-9]`, `[A-Za-z]` = classes de caractères
- `^` début, `$` fin
- `\.` pour chercher un point littéral
- `\d` = chiffre, `\w` = mot (lettres/chiffres/\_)

---

👉 Veux-tu que je prépare un **poster A4 simplifié “les regex en 10 exemples”** pour ton fils (un mémo qu’il pourra garder à côté de lui) ?
