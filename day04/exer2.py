

from myutils4 import scan_directory
from myutils4 import printListFile
from myutils4 import scan_dir2
from myutils4 import convert_files
from myutils4 import printMyFile
from myutils4 import writejson_file
from myutils4 import convert_path_to_filename
from myutils4 import readcsv_file
from myutils4 import writecsv_file

sdir = "/data/Python_cours02_avance/"
spattern = "*.md"

liste = scan_directory("/data/Python_cours02_avance/", "*.txt", True)

printListFile(liste)

l = convert_files(liste)

printMyFile(l)


soutput = convert_path_to_filename(sdir,".csv")

writecsv_file(soutput, l)


l2 = readcsv_file(soutput)
print("nb entrées: " + str(len(l2)))

