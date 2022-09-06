from turtle import fd
from distance_func import make_distance
import re
dir1='result/sorttest/AEI/AEI_15_0.csv'
dir2='result/sorttest/AEI/AEI_2_1.csv'
dir='result/sorttest/AEI'

import glob
import copy
dir11=glob.glob(dir+'/AEI_15_*csv')
dir22=glob.glob(dir+'/AEI_2_*csv')
fdis=100
for d1 in dir11:
    print(re.split('_',d1)[-1].replace('.csv',''),re.split('_',d)[-1].replace('.csv',''))
    dis=make_distance(d1,d)
    if fdis>=dis:
        
        fdis=copy.deepcopy(dis)
    print(dis)
print()
print(fdis)