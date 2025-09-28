Super 👍 allons-y pour le **Day 06**.
À ce stade, ton fils maîtrise les bases des listes/dicts → il est prêt à voir **comment organiser et centraliser du code avec des fonctions**, et à découvrir une **nouvelle lib de base** : `json` pour sauvegarder/charger le carnet.

---

# 📚 Day 06 — Centraliser le code avec des fonctions & JSON

---

## 🎯 Objectifs

- Comprendre pourquoi **factoriser** du code avec des fonctions.
- Découvrir la **syntaxe des fonctions avec paramètres** et `return`.
- Apprendre à utiliser les **f-strings** (`print(f"salut {nom}")`).
- Introduire la **lib `json`** pour persister les données.
- Améliorer le **Carnet numérique** avec sauvegarde/rechargement.

---

## 1) Pourquoi des fonctions ?

👉 Quand on répète du code, c’est :

- plus difficile à maintenir,
- plus facile à oublier de corriger partout.

💡 Exemple “mauvais” :

```python
print("Salut Alex")
print("Salut Marie")
print("Salut Sam")
```

💡 Exemple factorisé :

```python
def saluer(nom):
    print(f"Salut {nom}")

saluer("Alex")
saluer("Marie")
saluer("Sam")
```

---

## 2) Fonctions : paramètres et retour

```python
def addition(a: int, b: int) -> int:
    return a + b

print(addition(5, 3))   # 8
```

- Paramètres = données d’entrée.
- `return` = renvoie un résultat à réutiliser.

👉 On peut retourner plusieurs valeurs avec un tuple :

```python
def divmod_custom(a: int, b: int):
    return a // b, a % b

q, r = divmod_custom(10, 3)
print(q, r)  # 3 1
```

---

## 3) Les f-strings

- Syntaxe : `f"texte {variable}"`.
- Permet d’insérer des variables dans une chaîne.

Exemple :

```python
nom = "Alex"
age = 14
print(f"{nom} a {age} ans")   # Alex a 14 ans
```

---

## 4) La bibliothèque JSON

JSON ↔ Python = très naturel.

- `dict` ↔ objet JSON
- `list` ↔ tableau JSON
- `str`, `int`, `float`, `bool`, `None` ↔ types JSON équivalents

### Sauvegarder en JSON

```python
import json

contacts = [
    {"nom": "Alex", "age": 14, "tel": "123"},
    {"nom": "Marie", "age": 15, "tel": "456"},
]

with open("contacts.json", "w", encoding="utf-8") as f:
    json.dump(contacts, f, indent=2, ensure_ascii=False)
```

### Lire depuis JSON

```python
with open("contacts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data[0]["nom"])  # Alex
```

---

## 5) Exercices guidés

### Exo 1 — Fonction `carré`

Écrire une fonction `carre(x)` qui retourne le carré de `x`.

### Exo 2 — Retour multiple

Écrire `stats(liste)` qui retourne `(min, max, moyenne)`.

### Exo 3 — Sauvegarde JSON

Créer une liste de 3 contacts, l’écrire dans `contacts.json`, puis la relire et afficher les noms.

---

## 6) Fil rouge — Carnet numérique (Day 06)

### 6.1 Centraliser les fonctions

Créer un fichier `contacts.py` avec les fonctions :

- `ajouter_contact()`
- `afficher_contacts()`
- `import_liste()`

Puis dans `main.py` :

```python
from contacts import ajouter_contact, afficher_contacts, import_liste
```

### 6.2 Sauvegarde automatique

Ajouter deux fonctions :

```python
def sauvegarder(contacts, path="contacts.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def charger(path="contacts.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
```

### 6.3 Intégration menu

Dans `main.py` :

```python
contacts = charger()

# … le menu habituel …

elif choix == "6":
    sauvegarder(contacts)
    print("✅ Contacts sauvegardés dans contacts.json")
```

---

## 7) Résultat attendu en fin de Day 06

- Compréhension claire de l’intérêt des fonctions.
- Maîtrise des **f-strings**.
- Découverte et utilisation de **JSON** pour la persistance.
- Carnet numérique capable de **sauvegarder/recharger ses données** → première fois que le travail **reste d’une session à l’autre**.

---

👉 Veux-tu que je te génère un **starter kit Day 06** avec `contacts.py`, `main.py` (menu minimal) et un exemple `contacts.json` ?
