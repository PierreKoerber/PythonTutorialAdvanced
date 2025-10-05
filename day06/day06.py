
from myutils6 import readjson_file
from myutils6 import printMessage
from myutils6 import printSpacer

from myparser6 import fetch_page
from myutils6 import mylog

# print

printMessage("Ouvre un fichier qui n'existe pas")

readjson_file("toto22.json")

printSpacer()


# print parser error

fetch_page("www.xxffsafdsafa.com")


mylog("ceci est un message")
