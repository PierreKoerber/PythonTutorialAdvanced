
import random


import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def getRandomWord():
    words = ["ordinateur","python","programmation","algorithme","variable","fonction","bibliotheque","internet","serveur","client","navigateurs","base","donnees","logiciel","materiel","reseau","application","terminal","compilation","virtualisation"]
    i = random.randint(0, len(words))
    return words[i]

def lettres_trouvee_dans_mot(word, lettres_demandees):
    lettres = list(word)
    res = ""
    for lettre in lettres:
        if lettre in lettres_demandees:
            res = res + " " + lettre
        else:
            res = res + " _"
    return res

def hangman():
    nombre_essai = 10
    word = getRandomWord() 
    nombre_tentives = 0 
    lettres_demandees = []

    while(nombre_essai > nombre_tentives):
        #clear() 
        lettre = input("Votre lettre ?")
        # Test si lettre est correct
        # Test si 1 seule lettre
        # Test si lettre déjà demandée
        lettres_demandees.append(lettre)

        resultat = lettres_trouvee_dans_mot(word, lettres_demandees)
        print(resultat)
        print("il reste " +str(nombre_essai - nombre_tentives) )

        nombre_tentives = nombre_tentives + 1

    print("fin de la partie")
    
hangman()