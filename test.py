f=open('read_cryspy/init_poscars/ID_0_POSCAR.nnlist','r').readlines()
#print(r'{}'.format(f[0]),end=' ')
from collections import defaultdict
import re
import sys
nnlist=defaultdict(list)
import pandas as pd
for i in f:
    float_info=re.findall('\-*\d+\.?\d+',i)
    int_info=re.findall('\-*\d+',i)
    int_info=[int(int_info_) for int_info_ in int_info]
    float_info=[float(float_info_) for float_info_ in float_info]
    nnlist[tuple(int_info[0:2])].append((float_info[0],float_info[1::],int_info[-3::]))
isite=1
adjacent_num=4
for i in range(1,9,1):
    print((1,i))
    nnlist[(1,i)].sort(key=lambda x:x[0])
    a=nnlist[(1,i)][1:adjacent_num+1]
    md,mcoord,_=a[0]
    print(a[0])
    break

mcoord=[-1*mcoord_ for mcoord_ in mcoord]

for i in range(1,9,1):
    print('i=',i)
    nnlist[(1,i)].sort(key=lambda x:x[0])
    a=nnlist[(1,i)][1:adjacent_num+1]
    for ai in a:
        distance,coord,_=ai
        if coord==mcoord:
            print(ai)