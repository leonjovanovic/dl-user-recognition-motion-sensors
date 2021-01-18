import os
import re 
import math  
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Path50Hz";
list = os.listdir(path)

list

def removeEvery4Row(path,num):
    with open(path, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(path, 'w') as fout:
        for x in range(0, len(data), num):
            fout.writelines(data[x])
        
for count,filename in enumerate(os.listdir(path)): 
    print(filename)
    match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
    items = match.groups()
    if items[1]!="Output" and items[1]!="Recording":
        removeEvery4Row(path+"\\"+filename, 4)