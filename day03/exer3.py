from myutils3 import scan_directory
from myutils3 import printListFile
from myutils3 import scan_dir2
from myutils3 import filter_files_by_pattern

 
sdir = "/data/Python_cours02_avance/"
spattern = "*.md"


liste = scan_directory("/data/Python_cours02_avance/", "*.md", True)

printListFile(liste)


newlist = filter_files_by_pattern(liste, "day")


printListFile(newlist)
