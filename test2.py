from crystal_emd.make_cluster import make_cluster_dataset
from crystal_emd.cluster_adress_func import cluster_list
import subprocess
datasetdir='result/testcif/'
clusterlistdf=cluster_list(datasetdir,dirs=True)
allclusterlen=clusterlistdf.shape[0]
for i,data in clusterlistdf.iterrows():
    print('\r{} {}/{}'.format(data.cifid,i+1,allclusterlen),end='')
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    make_cluster_dataset(cifid=data.cifid,cluster_adress=clusteradress,outdir=data.adress)
    break