import pandas as pd
import re
import os
import glob

versionMatch ="(?<=VERSION_ID=)[A-Za-z0-9]+"
buildMatch = "(?<=BUILD_ID=)[A-Za-z0-9]+.\d+.\d+"

## Sort the files in logs dir and choose most recent BKC file
def sortBKC():
    dir = "logs"
    fileList = []
    os.chdir(dir)
    listFiles = sorted( filter(
        os.path.isfile,
        glob.glob("*_bkc.txt")), key=os.path.getctime, reverse=True)
    os.chdir("..")
    for file in listFiles:
        fileList.append(file)
    return fileList[0]

## Match version ID from bkc file
def versionID():
    fl = sortBKC()
    with open(f"logs/{fl}", 'r') as f:
        lines = f.readlines()
    for line in lines:
        match = re.search(versionMatch, line)
        if match:
            version = match.group()
            return version

## Match build ID from bkc file
def buildID():
    fl = sortBKC()
    with open(f"logs/{fl}", 'r') as f:
        lines = f.readlines()
    for line in lines:
        match = re.search(buildMatch, line)
        if match:
            version = match.group()
            return version

# verM = versionID()
# buildM = buildID()

## Replace captured variables inside PACs naming file
def bkcReplace(pattern, column):
    with open("pacs_kpi_naming.txt", 'r') as namef:
        kpis_file = namef.readlines()
    for line in kpis_file:
        kpis_f = re.split("(_*_)", line)
        oldstring = kpis_f[column]
        namef.close()

    with open("pacs_kpi_naming.txt", 'r') as namef:
        kpis_file = namef.read()
        if column == int(-5):
            pattern = str("R") + str(pattern)
            new = kpis_file.replace(oldstring, pattern)
        else:
            new = kpis_file.replace(oldstring, pattern)
            namef.close()

    with open("pacs_kpi_naming.txt", 'w') as namef:
        namef.write(new)
        namef.close()

# bkcReplace(verM,int(-5))
# bkcReplace(buildM,int(-3))


