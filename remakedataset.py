from crystal_emd.read_info import remake_csv
from crystal_emd.cluster_adress_func import cluster_list
import sys,os

d=make_sort_ciffile(datasetadress,estimecont='all')
datasetdir='cluster_dataset'
if os.path.isdir(datasetdir):
        shutil.rmtree(datasetdir)

#for sampleadress in d.sample(100,random_state=0).cifadress.to_list():
for i,sampleadress in enumerate(d.iloc[0:100].cifadress.to_list()):
    print('\r{}/100'.format(i+1),end='')
    copyadress='cluster_dataset/{}'.format(os.path.basename(sampleadress))
    if os.path.isdir(copyadress):
        shutil.rmtree(copyadress)
    shutil.copytree(sampleadress,copyadress)

clusterlistdf=cluster_list(datasetdir)
alllen=clusterlistdf.shape[0]*12
cont=0
print(clusterlistdf)
for i,data in clusterlistdf.iterrows() :
    for pattern in range(0,12):
        cont+=1
        adress='{}/{}_{}_{}.csv'.format(data.adress,data.cifid,data.isite,pattern)
        resultadress='{}/{}_{}_{}.csv'.format(datasetdir,data.cifid,data.isite,pattern)
        if not os.path.isfile(adress):
            continue
        #print(adress)
        remake_csv(adress,outname=resultadress)

from crystal_emd.read_info import make_sort_ciffile
import pandas as pd
from crystal_emd.read_info import Set_Cluster_Info
from crystal_emd.cluster_adress_func import cluster_list
import os,sys
datasetdir='cluster_dataset'

ciflistdf=make_sort_ciffile(datasetdir,estimecont='all')
allciflen=ciflistdf.shape[0]
for i,data in ciflistdf.iterrows():
    cifid=data.cifid
    print('\r{} {}/{}'.format(cifid,i+1,allciflen),end='')
    cont=0
    cwd=os.getcwd()
    clusterlist=cluster_list(data.cifadress)
    alllen_=0
    os.chdir(data.cifadress)
    for i2,data2 in clusterlist.iterrows():
        csvadress='{}_{}_0.csv'.format(data2.cifid,data2.isite)
        df=pd.read_csv(csvadress,index_col=0)
        cluster=Set_Cluster_Info(clusterdf=df)
        #alllen=alllen_*len(cluster.shaft_comb)
        isite=df.iloc[0].isite
        for pattern in range(len(cluster.shaft_comb)):
            cont+=1
            #print("\r"+str(cont)+'/'+str(alllen),end="")
            cluster.parallel_shift_of_center()
            cluster.rotation(pattern=pattern)
            cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
    os.chdir(cwd)


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