import os
import re 
import math  
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data";
list = os.listdir(path)

list

def remove_first_row(path1):
    p = path1
    with open(p, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(p, 'w') as fout:
        fout.writelines(data[0:11988])
        
for count,filename in enumerate(os.listdir(path)): 
    print(filename)
    match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
    items = match.groups()
    if items[1]!="Output" and items[1]!="Recording":
        remove_first_row(path+"\\"+filename)
            