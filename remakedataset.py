from crystal_emd.read_info import remake_csv
from crystal_emd.cluster_adress_func import cluster_list
import sys,os
datasetdir='cluster_dataset'
clusterlistdf=cluster_list(datasetdir,dirs=True)
clusterallen=clusterlistdf.shape[0]

for i,data in clusterlistdf.iterrows() :
    print('\r{} {}/{}'.format(data.cifid,i+1,clusterallen),end='')
    adress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    resultadress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    if not os.path.isfile(adress):
        continue
    #print(adress)
    remake_csv(adress,outname=resultadress)

'''
from crystal_emd.make_cluster import make_cluster_dataset
from crystal_emd.cluster_adress_func import cluster_list
import subprocess
datasetdir='cluster_dataset'
clusterlistdf=cluster_list(datasetdir,dirs=True)
allclusterlen=clusterlistdf.shape[0]
for i,data in clusterlistdf.iterrows():
    print('\r{} {}/{}'.format(data.cifid,i+1,allclusterlen),end='')
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    make_cluster_dataset(cifid=data.cifid,cluster_adress=clusteradress,outdir=data.adress)
'''


'''
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
'''