from gc import collect
from operator import index
import os
from turtle import left
import pandas as pd
from pathlib import Path
import glob
import shutil
import fnmatch
import re

#exceldir = ("C:\Users\ChromePnP\Desktop\excel_exchange")
cwd = os.getcwd()
rawdir = cwd+r"\raw"
files_rawdir = cwd+r"\raw\*\*R*_summary.csv"
procdir = cwd+r"\processed"
files_procdir = cwd+r"\processed\*R*"
final_dir = cwd+r"\finished"

#File path to where bulk excel spreadsheets are contained
#os.chdir(rawdir)
new_path = os.getcwd()

#verify new path is correct directory
print(new_path)

# move summary.csv files into processed directory
for f in glob.glob(files_rawdir, recursive=True):
    shutil.move(f, procdir)

#Copy and format the first run into new .csv files that will contain final run data.
collected = os.listdir(procdir)
flist = list(collected)
flist.sort()
first_file = flist[0]
print(first_file)

fname = re.split("(_*_)", first_file)
print (fname [2:16])
new_Fname = "".join(fname[2:-3])
print (new_Fname)
os.chdir(procdir)
rundata_file = shutil.copyfile(first_file, new_Fname + "rundata.csv" )

# Format and prepare copied file for run data inserted from processed .csv files 
f_template = pd.read_csv(rundata_file)
#f_template.drop(['Peak', '5s Peak', 'Peak Time', '1s Peak Time', '5s Peak Time'], inplace=True, axis=1)
f_template.drop(['Peak', '5s Peak', 'Peak Time', '5s Peak Time'], inplace=True, axis=1)
f_template.to_csv(rundata_file, index=False)

# Loop though .csv files and input 'Average' column into selected formatted file
rest_of_files = flist[1:]

#print(rest_of_files)

# Collect columns in remaining files 
num_col = (len(collected))
print ("Number of columns will be", num_col)

dfs = []
for f in rest_of_files:
    get_averages = pd.read_csv(f)
    dfs.append(pd.read_csv(f)['Average'])
    df = pd.concat(dfs, axis=1)

# Merge all columns final file
f2_temp = pd.read_csv(rundata_file)
merge_averages = pd.concat([f2_temp, df], axis=1, sort=True)
merge_averages.to_csv(rundata_file, index=False)

# Move finished file and clean processed directory
shutil.move(rundata_file, final_dir)

