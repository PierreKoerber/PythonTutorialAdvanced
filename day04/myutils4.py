
from pathlib import Path
import re
import re, fnmatch

import datetime
import json


def readcsv_file(file):
    # TO DO
    return 

def writecsv_file(file, row):
    # to do
    return 

def readjson_file(file):
    with open(file, "r", encoding="utf-8") as f:
        d = json.load(f)

def writejson_file(file, row):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
   

def writefile(filname, txt):
    f = open(filename, "w", encoding="UTF8")
    f.write(txt)
    f.close()

def readfile(filename):
    f = open(filename, "r", encoding="UTF8")
    txt = f.read()
    f.close()
    return txt



def scan_dir2(sdir, pattern):
    files = Path(sdir).glob("*.txt")
    return files 


def check_pattern(text, pattern):
    if any(ch in pattern for ch in "*?[]"):       # ça ressemble à une glob
        return fnmatch.fnmatch(text, pattern)
    return bool(re.search(pattern, text, re.IGNORECASE))



def scan_directory(folder, pattern="**/*", recur=False):
    liste = []

    if recur == True: 
        files = Path(folder).glob("**/*")
    else:
        files = Path(folder).iterdir()

    for f in files:
        if ( check_pattern(f.suffix, pattern) ):
            liste.append(f)

    return liste

def filter_files_by_pattern(files, pattern):
    newlist=[]
    pat = re.compile(pattern)
    for f in files:
        if pat.search(str(f)):
            newlist.append(f)
    return newlist

def filter_files_by_size(listefichier, sizeoctet):
    newlist = []
    for f in listefichier:
        if f.stat().st_size > sizeoctet:
            newlist.append(f)
    return newlist

def sort_by_date(listefile):
    return sorted(listefile, key=lambda x: x.stat().st_mtime)

def sort_by_size(listefile):
    return sorted(listefile, key=lambda x: x.stat().st_size)

def printListFile(liste,title=""):
    print("--------------------")
    print(title)
    for f in liste:
        print(f"Fichier : {f} - size={f.stat().st_size} - {format_mtime(f.stat().st_mtime)}" )

def format_mtime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)
    
