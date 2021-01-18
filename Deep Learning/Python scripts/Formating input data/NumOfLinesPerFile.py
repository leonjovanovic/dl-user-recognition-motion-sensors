import os
import re 
import math  
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data";
list = os.listdir(path)
min = 15000;

def findMin(path1,filename1, min):
    file1 = open(path1 +"\\"+ filename1, "r")
    lines = file1.readlines()       
    count = 0
    for line in lines: 
        count = count + 1
    if(count<min):
        min = count
    file1.close()
    return min

for count, filename in enumerate(os.listdir(path)): 
    match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
    items = match.groups()
    if items[1]!="Output" and items[1]!="Recording":
        min = create_vec(path,filename,min)
            
