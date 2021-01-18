import os
import re 
import math  
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data";
list = os.listdir(path)

def create_vec(path,filename):
    file1 = open(path +"\\"+ filename, "r") 
    file2 = open(path +"\\"+ "vector" + filename, "w") 
    
    lines = file1.readlines()       
    count = 0
    for line in lines: 
        numbers = re.split("\t|\n", line)
        vector = math.sqrt(float(numbers[0])**2 + float(numbers[1])**2 + float(numbers[2])**2)
        file2.write(str(vector)+ '\r')
        print(vector)
        
    file1.close() 
    file2.close()

for count, filename in enumerate(os.listdir(path)): 
    match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
    items = match.groups()
    if items[1]!="Output" and items[1]!="Recording":
        create_vec(path,filename)
            
