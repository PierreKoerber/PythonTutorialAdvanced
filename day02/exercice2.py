
from myutils import scan_directory
from myutils import readfile

dossier = "/data/docarchiver3"

files = scan_directory(dossier, ".php", True)


for f in files:
    print(f) 
    print(readfile(f))