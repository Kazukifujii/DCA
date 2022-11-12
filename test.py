from crystal_emd.read_info import make_sort_ciffile,Set_Cluster_Info
from crystal_emd.cluster_adress_func import cluster_list
import os,re
diradress='cluster_dataset'
#remakediradress='{}_si'.format(diradress)
cifdirsdf=cluster_list(diradress,dirs=True)

import pandas as pd
cwd = os.getcwd()

for i,data in cifdirsdf.iterrows():
    cifid=data.cifid
    isite=data.isite
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,cifid,isite)
    if not os.path.isfile(clusteradress):
        print('not file {}'.format(clusteradress))
    clusterdf=pd.read_csv(clusteradress,index_col=0)
    cluster=Set_Cluster_Info(clusterdf=clusterdf)
    alllen=len(cluster.shaft_comb)
    for pattern in range(len(cluster.shaft_comb)):
        print('\r{}\n{}/{}'.format(cifid,pattern+1,alllen),end='')
        #cluster.parallel_shift_of_center()
        cluster.rotation(pattern=pattern)
        cluster.cluster_coords.to_csv('{}/{}_{}_{}.csv'.format(data.adress,cifid,isite,pattern))
print()
