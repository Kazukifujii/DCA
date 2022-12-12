
from crystal_emd.cluster_adress_func import cluster_list
atom_num=4
datasetdir='cluster_dataset'
listdf=cluster_list(datasetdir,dirs=True)
import os
for i,data in listdf.iterrows():
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    if not os.path.isfile(clusteradress):
        print('no file',clusteradress)
        continue
    index_num=int(open(clusteradress,'r').readlines()[-1][0])
    if index_num!=atom_num:
        print(clusteradress)
        os.remove(clusteradress)