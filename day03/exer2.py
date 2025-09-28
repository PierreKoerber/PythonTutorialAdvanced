



from myutils3 import scan_directory
from myutils3 import printListFile
from myutils3 import scan_dir2
from myutils3 import filter_files_by_size

sdir = "/data/Python_cours02_avance/"
spattern = "*.md"


liste = scan_directory("/data/Python_cours02_avance/", "*.md", True)

printListFile(liste)

listfiltree = filter_files_by_size(liste, "<",2000)


printListFile(listfiltree)
