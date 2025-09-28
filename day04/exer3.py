

from myutils4 import scan_directory
from myutils4 import printListFile
from myutils4 import scan_dir2
from myutils4 import convert_files
from myutils4 import readjson_file
from myutils4 import writejson_file
from myutils4 import convert_path_to_filename

sdir = "/data/Python_cours02_avance/"



soutput = convert_path_to_filename(sdir,".json")

l = readjson_file(soutput)

print(l)

print("nb entrées: " + str(len(l)))

 