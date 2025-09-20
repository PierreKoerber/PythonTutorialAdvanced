




from myutils import writefile,readfile

phrase = input("saisir une phrase :")

filename = "demo.txt"

writefile(filename, phrase)

ph2 = readfile(filename)

print(f"contenu du fichier {ph2}" )

