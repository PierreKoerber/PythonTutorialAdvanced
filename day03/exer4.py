from myutils3 import scan_directory
from myutils3 import printListFile
from myutils3 import scan_dir2
from myutils3 import filter_files_by_pattern
from myutils3 import sort_by_date
 
from myutils3 import sort_by_size

sdir = "/data/Python_cours02_avance/"
spattern = "*.md"


liste = scan_directory("/data/Python_cours02_avance/", "*.md", True)

printListFile(liste)

newlist = sort_by_date(liste)

printListFile(newlist, "trié par date")


newlist = sort_by_size(liste)

printListFile(newlist, "trié par taille")
