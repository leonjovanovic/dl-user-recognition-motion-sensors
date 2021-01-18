import numpy as np
import os
import re 
import math  

def output_enums(s):
    if(s == "BgNoise"):
        return 0
    if(s == "Lang"):
        return 1
    if(s == "Dist"):
        return 2
    if(s == "#Pers"):
        return 3
    if(s == "#M"):
        return 4
    if(s == "#F"):
        return 5
    if(s == "Y"):
        return 6
    if(s == "L/W"):
        return 12
    
def language_mapping(s):
    if(s == "Serbian"):
        return 0
    if(s == "English"):
        return 1
    if(s == "German"):
        return 2
    return -1;

def years_mapping(y):
    if(int(y) < 18):
        return 0
    if(int(y) > 30):
        return 2
    else:
        return 1

def words_mapping(w):
    if(w == 'a'):
        return 0
    if(w == "knjiga"):
        return 1
    if(w == "learning"):
        return 2
    if(w == "schmetterling"):
        return 3
    else:
        return 4
    
def noise_mapping(n):
    if(float(n)<0.25):
        return 0
    if(float(n)>=0.25 and float(n)<0.5):
        return 1
    if(float(n)>=0.5 and float(n)<0.75):
        return 2
    if(float(n)>=0.75):
        return 3
    
def distance_mapping(d):
    if(d == "0-2"):
        return 0
    if(d == "3-5"):
        return 1
    if(d == "5+"):
        return 2
    
def create_output(path, output_type):    
    path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data50Hz"
    data_labels = np.zeros((315,1))
    j=0
    out = output_enums(output_type)
    for count,filename in enumerate(os.listdir(path)):
        match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
        items = match.groups()
        if items[1]=="Output":
            with open(path+"\\"+filename, 'r') as fin:
                data = fin.read().splitlines(True)
            items = re.split("\t|\n",data[1])   
            data_labels[j,0] = language_mapping(items[out])#int(items[out])-1#------------------------------------------
            #print(int(items[out])-1)
            if(j == 290): 
                print(filename)
            j = j+1;
    return data_labels

def create_input(path, input_type):
    i = 0
    data_examples = np.zeros((315,2997,3))   
    for count,filename in enumerate(os.listdir(path)):
        match = re.match(r"([0-9]+)([a-zA-Z]+)", filename, re.I)
        items = match.groups()
        if items[1]==input_type:
            with open(path+"\\"+filename, 'r') as fin:
                data = fin.read().splitlines(True)
            for x in range(0, len(data), 1):
                items = re.split("\t|\n",data[x])
                items = items[:len(items)-1]
                data_examples[i,x,0] = float(items[0])
                data_examples[i,x,1] = float(items[1])
                data_examples[i,x,2] = float(items[2])
            i = i+1;
    return data_examples  

def create_vector_input(path, input_type):
    i = 0
    data_examples = np.zeros((315,2997))   
    for count,filename in enumerate(os.listdir(path)):
        match = re.match(r"(vector)([0-9]+)([a-zA-Z]+)", filename, re.I)
        items = match.groups()
        if items[2]==input_type:
            #print(filename)
            with open(path+"\\"+filename, 'r') as fin:
                data = fin.read().splitlines(True)
            for x in range(0, len(data), 1):
                data_examples[i,x] = float(data[x])
            i = i+1;
    len(data)
    return data_examples 

def create_dataset(path, input_type, output_type):
    data_examples = create_input(path, input_type)
    data_labels = create_output(path, output_type)
    return (data_examples, data_labels)

def create_vector_dataset(path, input_type, output_type):
    data_examples = create_vector_input(path, input_type)
    data_labels = create_output(path, output_type)
    return (data_examples, data_labels)  
    
    
    
    
    
    
    