
from pathlib import Path

def writefile(filname, txt):
    f = open(filename, "w", encoding="UTF8")
    f.write(txt)
    f.close()

def readfile(filename):
    f = open(filename, "r", encoding="UTF8")
    txt = f.read()
    f.close()
    return txt
 
def scan_directory(folder, pattern, recur):
    liste = []
    if recur == True: 
        files = Path(folder).glob("**/*")
    else:
        files = Path(folder).iterdir()

    for f in files:
        if (f.suffix == pattern):
            liste.append(f)

    return liste