import os
import re
path = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data";
list = os.listdir(path)

list

for count, filename in enumerate(os.listdir(path)): 
        name_sep=re.split(r'(\d+)', filename)
        new_name = name_sep[1]+name_sep[0]+name_sep[2]
        src = path + "\\" +filename
        dst = path + "\\" +new_name
        os.rename(src, dst) 