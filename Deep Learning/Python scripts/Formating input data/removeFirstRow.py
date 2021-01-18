import os
import re 
import math  
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data";
list = os.listdir(path)

list

def allignFiles(path):
    with open(path, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(path, 'w') as fout:
        fout.writelines(data[0:11988])
        
for count,filename in enumerate(os.listdir(path)):
    match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
    items = match.groups()
    if items[1]!="Output" and items[1]!="Recording":
        allignFiles(path+"\\"+filename)
            