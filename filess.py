# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:26:22 2020

@author: lalitha
"""

import os,sys
import numpy as np


path = 'D:/DanCarter/'

## Array to save files
files1=[]

##Array to save directories
direc =[]

##Get Subsirectories array
sub_dir =[]
##Initialize dictionary
newdic ={}
##All files and directories in path listed
files = os.listdir(path)

for name in files:
    full_path = os.path.join(path, name)
    if os.path.isdir(full_path):
        #print(full_path,', dir')
        direc=np.append(direc,full_path)
       
    if os.path.isfile(full_path):
        #print(full_path,', file')
        files1 = np.append(files1,full_path)
##Sved as CSV to see values       
np.savetxt("D:/Lalitha Files/filesxx.csv", direc, delimiter=",",fmt='%s')
       
##walk through all directories
for dirpath, dirname, filename in os.walk(path):
    ##Create Dictionary
    newdic[dirpath] = filename
    
    ##Save Subdirectories path
    sub_dir = np.append(sub_dir,dirpath)

##Iter through the dictionary
for name in direc:
    array = []
    for name2 in sub_dir:
        if name in name2:
            Foo = newdic.get(str(name2))
            array = np.append(array,Foo)
            
    ##Save CSV for every directory
    np.savetxt("D:/Lalitha Files/file_Stat"+str(nnn)+".csv",
               array,delimiter=",",fmt='%s')
    
    ##counter for saving reference
    nnn = nnn+1
 

            
            