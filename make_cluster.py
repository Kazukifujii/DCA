from operator import index
import os,pickle
import subprocess
from read_info import Set_Cluster_Info

#mast run test1.py,test2.py
from read_info import clusterplot as clp
import re
"""
resultdir='result/sorttest'
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(resultdir))
cifdir = cifdir_.split('\n')
del cifdir[0]
"""
dir='/home/fujikazuki/crystal_emd/result/allzeorite'
import pandas as pd
cifdir=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
cwd = os.getcwd()
for i in cifdir:
    cifid=os.path.basename(i)
    print(cifid)
    cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(i))
    with open(cifdir_nn_i_data,"rb") as frb:
        nn_data = pickle.load(frb)
    alllen_=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            alllen_+=1
    cont=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            cluster=Set_Cluster_Info(isite,nn_data,4)
            alllen=alllen_*len(cluster.shaft_comb)
            for pattern in range(len(cluster.shaft_comb)):
                os.chdir(i)
                cont+=1
                print("\r"+str(cont)+'/'+str(alllen),end="")
                cluster.parallel_shift_of_center()
                cluster.rotation(pattern=pattern)
                cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
                os.chdir(cwd)
    print()
