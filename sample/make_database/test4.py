from subprocess import run
import os,pickle,subprocess,re
import sys
from crystal_emd.read_info import make_sort_ciffile
import pandas as pd
from glob import glob as gl
datasetdir="cluster_dataset"

from crystal_emd.make_cluster import make_cluster_dataset

picdata=make_sort_ciffile(datasetdir,estimecont='all')
cwd = os.getcwd()
allciflen=picdata.shape[0]
for i,data in picdata.iterrows():
    print('\r{} {}/{}'.format(data.cifid,i+1,allciflen),end='')
    nn_data_adress= subprocess.getoutput("find {0} -name nb_*.pickle".format(data.cifadress))
    #make_cluster_dataset(cifid=data.cifid,nn_data_adress=nn_data_adress,adjacent_num=2,outdir=data.cifadress)

from crystal_emd.cluster_adress_func import cluster_list
atom_num=8
datasetdir='cluster_dataset'
listdf=cluster_list(datasetdir,dirs=True)
import os
from glob import glob
for i,data in listdf.iterrows():
    csvlist=glob('{}/{}_{}_[0-9]*.csv'.format(data.adress,data.cifid,data.isite))
    #clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    for clusteradress in csvlist:
        if not os.path.isfile(clusteradress):
            print('no file',clusteradress)
            continue
        index_num=int(open(clusteradress,'r').readlines()[-1][0])
        if index_num!=atom_num:
            print(clusteradress)
            os.remove(clusteradress)
print('end creanup')
#cifdir=pd.read_csv('{}/picupadress'.format(datasetdir),index_col=0)
cwd = os.getcwd()
errorid=list()
cont=0
from crystal_emd.cluster_adress_func import isite_list
from crystal_emd.distance_func import make_distance_csv,remake_distance
from crystal_emd.clustering_func import make_clusering
for i,data in picdata.iterrows():
    cifid=data.cifid
    print(cifid)
    listadress_=isite_list(data.cifadress)
    make_distance_csv(listadress=listadress_,resultname="{}/{}_self_distance".format(data.cifadress,cifid))
    remake_distance("{}/{}_self_distance".format(data.cifadress,cifid))
    flusterdf=make_clusering(csvadress="{}/{}_self_distance_remake".format(data.cifadress,cifid),csvn="{}/{}_sort_distance".format(data.cifadress,cifid),pngn='{}/{}_self_distance.png'.format(data.cifadress,cifid))
    flusterdf.to_csv("{}/{}_fcluster".format(data.cifadress,cifid))


#reduce dataset
from crystal_emd.cluster_adress_func import fcluster_list
resultdir='database'
orignal_dataset='cluster_dataset'
fclusterdf=fcluster_list(orignal_dataset)
import shutil,os

if os.path.isdir(resultdir):
    shutil.rmtree(resultdir)

os.mkdir(resultdir)
for i,data in fclusterdf.iterrows():
    for pattern in range(12):
        clusteradress='{}/{}_{}_{}.csv'.format(data.adress,data.cifid,data.isite,pattern)
        if not os.path.isfile(clusteradress):
            print('not file ',clusteradress)
        copyadress='{}/{}_{}_{}.csv'.format(resultdir,data.cifid,data.isite,pattern)
        shutil.copy(clusteradress,copyadress)