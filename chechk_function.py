from Distance_based_on_Cluster_Analysis.clustering_func import make_clusering
import pandas as pd

#isitelist=pd.read_csv('DCA/result/cifdirs/WEN/WEN_self_distance',index_col=0)
import os
#os.chdir('result/cifdirs/JOZ')
#make_clusering(csvadress='result/cifdirs/WEN/WEN_self_distance',csvn='result/cifdirs/WEN/WEN_sort_distance')
cifdir='cifdirs'
cluster_atom_num=8
import subprocess
adjacent_num=2
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
picdata=make_sort_ciffile('result/{}'.format(cifdir),estimecont='all')
cwd = os.getcwd()
allciflen=picdata.shape[0]

for i,data in picdata.iterrows():
    print('\r{} {}/{}'.format(data.cifid,i+1,allciflen),end='')
    nn_data_adress= subprocess.getoutput("find {0} -name nb_*.pickle".format(data.cifadress))
    make_cluster_dataset(cifid=data.cifid,adjacent_num=adjacent_num,nn_data_adress=nn_data_adress,outdir=data.cifadress,rotation=False)
print('')
from Distance_based_on_Cluster_Analysis.cluster_adress_func import cluster_list
listdf=cluster_list('result/{}'.format(cifdir),dirs=True)
f=open('clean up_cluster.log','w')
for i,data in listdf.iterrows():
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    if not os.path.isfile(clusteradress):
        print('no file',clusteradress)
        continue
    index_num=int(open(clusteradress,'r').readlines()[-1][0])
    if index_num!=cluster_atom_num:
        f.write('{}\n'.format(clusteradress))
        os.remove(clusteradress)
f.close()
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
listdf=cluster_list('result/{}'.format(cifdir),dirs=True)

for i,data in listdf.iterrows():
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    make_cluster_dataset(cluster_adress=clusteradress,outdir=data.adress)
print('')