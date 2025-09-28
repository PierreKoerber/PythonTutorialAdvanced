Parfait ! Voici un **Day 05** prêt à dérouler — on consolide à fond **Listes** et **Dictionnaires** et on fait avancer le **fil rouge “Carnet numérique”**.

---

# 📚 Day 05 — Listes & Dictionnaires (maîtrise)

## 🎯 Objectifs

- Savoir créer, modifier, parcourir **listes** et **dictionnaires**.
- Comprendre quand utiliser l’un ou l’autre.
- Pratiquer les méthodes essentielles.
- Faire évoluer le **Carnet** : affichage propre, tri de base, import minimal.

---

## 1) Rappel express

### Listes (`list`)

- Ordonnées, **modifiables**

```python
scores = [100, 150, 90]
scores.append(120)
scores.remove(90)
val = scores.pop()        # retire le dernier et le retourne
scores2 = sorted(scores)  # retourne une nouvelle liste triée
scores.sort(reverse=True) # trie sur place
```

### Dictionnaires (`dict`)

- Paires **clé → valeur**, accès par clé, **modifiable**

```python
joueur = {"pseudo": "Alex", "score": 150}
joueur["level"] = 3       # ajout
joueur["score"] = 200     # modif
del joueur["level"]       # suppression
for k, v in joueur.items():
    print(k, v)
```

---

## 2) Méthodes utiles (mémo)

### list

- `append(x)`, `extend(iterable)`, `insert(i,x)`
- `remove(x)`, `pop([i])`, `clear()`
- `sort(key=None, reverse=False)`, `reverse()`
- `count(x)`, `index(x)`, `copy()`

### dict

- `get(cle, defaut)`, `keys()`, `values()`, `items()`
- `pop(cle[, defaut])`, `update({...})`
- Test d’existence : `"score" in joueur`

---

## 3) Exercices guidés (rapides)

### Exo 1 — Nettoyage & tri

```python
noms = ["alex", "marie", "sam", "alex", "zoe"]
# 1) mettre en majuscules la première lettre
# 2) supprimer les doublons
# 3) trier alphabétiquement
```

_Indications_ : `title()`, `set()`, `sorted()`.

### Exo 2 — Liste de dicts

```python
joueurs = [
   {"pseudo": "Alex", "score": 150},
   {"pseudo": "Marie", "score": 210},
   {"pseudo": "Sam", "score": 180},
]
# 1) afficher "Marie - 210"
# 2) trier par 'score' décroissant
# 3) récupérer le meilleur joueur
```

_Indications_ : `sorted(joueurs, key=lambda j: j["score"], reverse=True)`.

### Exo 3 — Index simple de mots

```python
texte = "le chat mange la souris et le chat dort"
# construire un dict {mot: compteur}
```

_Indications_ : `split()`, boucle, `dict.get(mot, 0)+1`.

---

## 4) Fil rouge — Carnet numérique (évolutions Day 05)

### 4.1 Affichage propre + tri

Créer une fonction **`afficher_contacts(contacts, sort_key="nom", desc=False)`** :

```python
def afficher_contacts(contacts: list[dict], sort_key="nom", desc=False) -> None:
    if not contacts:
        print("Aucun contact.")
        return
    tries = sorted(contacts, key=lambda c: c.get(sort_key, ""), reverse=desc)
    print("\n--- Contacts ---")
    for c in tries:
        nom = c.get("nom", "?")
        age = c.get("age", "?")
        tel = c.get("tel", "?")
        print(f"- {nom:15} | {age:3} ans | {tel}")
```

### 4.2 Ajout “robuste” (petit pas)

Normaliser le nom et le téléphone dans **`ajouter_contact`** :

```python
def ajouter_contact(contacts: list[dict], nom: str, age: int, tel: str) -> None:
    contact = {
        "nom": nom.strip().title(),
        "age": int(age),
        "tel": tel.strip().replace(" ", "")
    }
    contacts.append(contact)
```

### 4.3 Mini-import depuis une liste simple

Ajouter une fonction **`import_liste(lines)`** qui prend des lignes `"Nom,Age,Tel"` :

```python
def import_liste(contacts: list[dict], lines: list[str]) -> int:
    n = 0
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            continue
        nom, age, tel = parts
        try:
            ajouter_contact(contacts, nom, int(age), tel)
            n += 1
        except ValueError:
            pass
    return n
```

_Usage_ : pratique pour coller 3–5 lignes d’un coup.

---

## 5) Intégration menu (extrait `main.py`)

Ajouter 2 entrées :

- **2bis)** Afficher trié (par `nom` ou `age`)
- **5)** Importer des contacts collés (coller plusieurs lignes “Nom,Age,Tel”, finir par ligne vide)

```python
elif choix == "2":
    afficher_contacts(contacts)  # tri par défaut (nom)
elif choix == "2b":
    cle = input("Trier par (nom/age/tel) : ").strip() or "nom"
    desc = input("Décroissant ? (o/n) : ").lower().startswith("o")
    afficher_contacts(contacts, sort_key=cle, desc=desc)

elif choix == "5":
    print("Colle des lignes 'Nom,Age,Tel'. Ligne vide pour terminer :")
    lignes = []
    while True:
        s = input()
        if not s.strip():
            break
        lignes.append(s)
    ajoutes = import_liste(contacts, lignes)
    print(f"✅ {ajoutes} contact(s) importé(s).")
```

_(Adapte les numéros au menu réel de ton projet.)_

---

## 6) Exercices “après-cours”

1. **Filtre par âge**
   Écrire `filtrer_contacts(contacts, age_min=None, age_max=None)` qui renvoie une **nouvelle liste** filtrée.

2. **Mise à jour**
   Écrire `maj_contact(contacts, nom, tel=None, age=None)` qui modifie le contact si trouvé (retourne `True/False`).

3. **Top N par âge**
   Afficher les **N** plus âgés : `top_par_age(contacts, n=3)` → retourne la sous-liste triée par âge décroissant.

4. **Exporter un “rapport texte”**
   Créer `rapport(contacts, path="rapport.txt")` : écrire un résumé (nb de contacts, moyenne d’âge si possible, top 3 plus âgés).

---

## 7) Résultat attendu en fin de Day 05

- Tu sais **créer/transformer** des listes/dicts à la volée.
- Le **Carnet** affiche proprement et **peut trier**.
- Tu sais **importer** rapidement plusieurs contacts.
- Tu es prêt pour **S6/S7** (robustesse + stats/Counter) et la suite du fil rouge.
