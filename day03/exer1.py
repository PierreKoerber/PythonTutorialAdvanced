

from myutils3 import scan_directory
from myutils3 import printListFile
from myutils3 import scan_dir2




sdir = "/data/Python_cours02_avance/"
spattern = "*.md"

liste = scan_directory("/data/Python_cours02_avance/", "*.txt", True)

printListFile(liste)


liste2 = scan_dir2(sdir, "*.txt")

printListFile(liste2)
