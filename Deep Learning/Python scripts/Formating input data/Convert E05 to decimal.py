import os
import re 
import math  
import decimal
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data - Copy - Copy";
list = os.listdir(path)

def replaceToFloat(text):
    spliting = re.split('E-|\t|\n',text)
    power = int(spliting[1]) #Broj nakon E-0 koji govori koliko decimala treba da dodamo
    num = float(spliting[0]) #Broj pre E-0  
    d = decimal.Decimal(spliting[0]) #Broj decimala
    n = abs(d.as_tuple().exponent)+power #Ukupan br decimala
    s= "{:."+str(n)+"f}" #Formatiramo da fiksiramo ukupan broj decimala
    final = s.format(float(num/(10**power))) #Dobijamo konačan broj
    return final

def convert(path1,filename1):
    file = open(path1 +"\\"+ filename1, "r+") #Otvori fajl
    #read    
    lines = file.readlines() #Uzmi sve linije
    count = 0
    rewrite = ""
    for line in lines: #Uzimaj liniju po liniju
        if(re.search('E-0', line)): //Ukoliko sadrži format koji tražimo
            print(filename1)
            numbers = re.split("\t|\n", line)
            line = ""
            if(re.search('E', numbers[0])): #Ako se nalazi na X osi
                line += replaceToFloat(numbers[0]) + '\t'
            else:
                line += numbers[0] + '\t'
            if(re.search('E', numbers[1])): #Ako se nalazi na Y osi
                line += replaceToFloat(numbers[1]) + '\t'
            else:
                line += numbers[1] + '\t'
            if(re.search('E', numbers[2])): #Ako se nalazi na Z osi
                line += replaceToFloat(numbers[2]) + '\n'
            else:
                line += numbers[2] + '\n'
                
        rewrite += line
    file.close()

for count, filename in enumerate(os.listdir(path)): #Uzima sve nazive fajlova sa navedenih putanja
    match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I) #Deli naziv na brojeve i slova
    if(match):
        items = match.groups()
        if items[1]!="Output" and items[1]!="Recording": #Ako je fajl sa koordinatama
            convert(path,filename)
            








