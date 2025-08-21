Super 👍 tu veux donc un **plan détaillé** pour une séance type **S1 — Types & opérations de base** (après les 10 jours, quand tu reprends plus lentement).
Je te propose un **cours structuré** avec théorie + exemples + exercices + fil rouge.

---

# 📘 Cours S1 — Types & opérations de base (révision approfondie)

---

## 🎯 Objectifs

- Maîtriser les objets fondamentaux de Python (`str`, `list`, `dict`, `set`, `tuple`).
- Savoir utiliser les méthodes principales (notamment sur les chaînes et les listes).
- Comprendre le slicing et le tri (`sorted()`, `key=`, `reverse=`).
- Préparer le fil rouge : construire un **prototype d’index** (texte → liste de mots triés).

---

## 1) Les objets fondamentaux en Python

| Type    | Définition                  | Exemple                        | Particularité                            |
| ------- | --------------------------- | ------------------------------ | ---------------------------------------- |
| `str`   | Chaîne de caractères        | `"Bonjour"`                    | immuable, méthodes utiles                |
| `list`  | Liste ordonnée              | `[1, 2, 3]`                    | modifiable                               |
| `tuple` | Liste **immuable**          | `(1, 2, 3)`                    | fixe, plus sûr, clé de dict possible     |
| `dict`  | Dictionnaire (clé → valeur) | `{"nom": "Pierre", "age": 14}` | clé unique                               |
| `set`   | Ensemble (sans doublon)     | `{1, 2, 3}`                    | pas d’ordre, utile pour tester l’unicité |

---

## 2) Méthodes clés

### Chaînes (`str`)

- `.lower()`, `.upper()`
- `.strip()`
- `.split(" ")`
- `.replace("a","b")`
- `len("abc")`

### Listes (`list`)

- `.append(x)`
- `.extend([…])`
- `.remove(x)`
- `.pop(i)`
- `.sort()`, mais préférer `sorted(liste, key=…, reverse=…)`

### Dictionnaires (`dict`)

- `.keys()`, `.values()`, `.items()`
- accès par `d["clé"]` et `d.get("clé", valeur_par_défaut)`

### Sets (`set`)

- Opérations ensemblistes : `|` union, `&` intersection, `-` différence
- Vérifier appartenance : `x in mon_set`

---

## 3) Slicing (listes et chaînes)

```python
texte = "Bonjour"
print(texte[0:3])  # "Bon"
print(texte[:4])   # "Bonj"
print(texte[-2:])  # "ur"

liste = [10,20,30,40,50]
print(liste[1:4])  # [20,30,40]
print(liste[::-1]) # inverse [50,40,30,20,10]
```

---

## 4) Tri avec `sorted()`

```python
nombres = [5,2,9,1]
print(sorted(nombres))                # [1,2,5,9]
print(sorted(nombres, reverse=True))  # [9,5,2,1]

mots = ["chat","elephant","zèbre","rat"]
print(sorted(mots, key=len))  # trie par longueur
```

---

## 5) Exercices pratiques

### Exo 1 — Compter les mots

- Demander une phrase.
- La découper avec `.split()`.
- Compter la fréquence de chaque mot avec un `dict`.
- Afficher le top N mots avec `sorted()`.

👉 Exemple :

```python
phrase = "le chat mange la souris et le chat dort"
# résultat attendu : {"le":2,"chat":2,"mange":1,"souris":1,"et":1,"dort":1}
```

### Exo 2 — Supprimer doublons

- À partir d’une liste avec répétitions, utiliser un `set` pour enlever les doublons.

### Exo 3 — Slicing

- Extraire les 3 premiers et les 3 derniers mots d’une phrase.

---

## 6) Fil rouge (index prototype)

🎯 Construire un **petit index de mots** à partir d’un texte :

1. Lire une phrase ou un petit paragraphe (input ou fichier texte).
2. Transformer en liste de mots (`split()`, nettoyage).
3. Créer une **liste de dictionnaires**, par ex. :

```python
[
  {"mot": "chat", "longueur": 4},
  {"mot": "chien", "longueur": 5}
]
```

4. Trier la liste avec `sorted()` selon :

   - ordre alphabétique
   - longueur
   - fréquence (exercice avancé)

👉 Ce sera la **base du futur moteur d’indexation** (cycle complet).

---

## 7) Récapitulatif de la séance

- Tu connais les **5 types fondamentaux**.
- Tu sais utiliser les **méthodes clés** sur `str`, `list`, `dict`, `set`.
- Tu as appris le **slicing** et le **tri avancé** avec `sorted()`.
- Tu poses la première brique du **fil rouge : indexer du texte**.

---

Veux-tu que je prépare aussi le **script corrigé** des exercices (exos 1 à 3 + fil rouge minimal) pour que ton fils puisse comparer son code ?
