


from myutils5 import print_with_label

joueur = {"pseudo": "Alex", "score": 150, "age":23}


print_with_label("get > ", joueur.get("pseudo"))


print_with_label("keys() >", joueur.keys())

for k in joueur.keys():
    print_with_label("   " + k + " => ",  joueur.get(k))


print_with_label("values >", joueur.values() )

print_with_label("items >", joueur.items())

#joueur.update( {"firstname": "pierre", "lastname:"koerber"} )


s = "pierre"
print(s.capitalize())

noms = ["alex", "marie", "sam", "alex", "zoe"]


for x in noms.sort():
    noms.set(x) = x.capitalize()

print(noms)