from collections import defaultdict
import re
import sys
import pickle
def make_nn_data_from_nnlist(fileadress,siteinfo):
    #set init info
    f=open(fileadress,'r').readlines()
    filename=re.split('/',fileadress)[-1]
    resultfile='{}.pickle'.format(filename.replace('.nnlist',''))
    resultadress=filename.replace(filename,'')
    resultadress='{}/{}'.format(resultadress,resultfile)
    nnlist=defaultdict(list)
    #read nnlist
    for i in f:
        float_info=re.findall('\-*\d+\.?\d+',i)
        int_info=re.findall('\-*\d+',i)
        int_info=[int(int_info_) for int_info_ in int_info]
        float_info=[float(float_info_) for float_info_ in float_info]
        nnlist[int_info[0]].append((int_info[1],float_info[0],float_info[1::],int_info[-3::]))
    #sort
    for i in nnlist.keys():
        nnlist[i].sort(key=lambda x:x[1])
        nnlist[i]=nnlist[i][1:5]
    #set nn_data
    nn_data=defaultdict(list)
    center_info=[sitinfo[0],1.0,0,0,0]
    for i in nnlist.keys():
        nn_data[i].append(center_info)
        for isite,distace,coord,cell in nnlist[i]:
            nn_data_=[isite,siteinfo[isite-1],*coord]
            nn_data[i].append(nn_data_)
    with open(resultadress,'wb') as f:
        pickle.dump(nn_data,f)
    return

fileadress='read_cryspy/init_poscars/ID_0_POSCAR.nnlist'
sitinfo=['Si' for _ in range(8)]
make_nn_data_from_nnlist(fileadress,siteinfo=sitinfo)