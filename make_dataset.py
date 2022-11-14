from subprocess import run
import os,pickle,subprocess,re
import sys
from crystal_emd.read_info import Set_Cluster_Info,make_sort_ciffile
import pandas as pd
from glob import glob as gl
cifdir="cluster_dataset"
resultdir=cifdir
'''
run('python3 crystal_emd/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,resultdir),shell=True)
print('emd make_adjacent_tabel')
run('python3 crystal_emd/make_nn_data.py --output2 {}'.format(resultdir),shell=True)
print('emd make_nn_data')
'''
from crystal_emd.make_cluster import make_cluster_dataset

picdata=make_sort_ciffile(cifdir,estimecont='all')
cwd = os.getcwd()
allciflen=picdata.shape[0]
for i,data in picdata.iterrows():
    print('\r{} {}/{}'.format(data.cifid,i+1,allciflen),end='')
    nn_data_adress= subprocess.getoutput("find {0} -name nb_*.pickle".format(data.cifadress))
    make_cluster_dataset(cifid=data.cifid,nn_data_adress=nn_data_adress,rotation=False,outdir=data.cifadress)