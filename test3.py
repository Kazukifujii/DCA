from crystal_emd.make_cluster import make_cluster_dataset
from glob import glob
import os
nnadress=glob('result/allzeorite/ABW/*pickle')[0]
make_cluster_dataset(cifid='ABW',nn_data_adress=nnadress,outdir=os.path.dirname(nnadress),rotation=False)
from crystal_emd.read_info import remake_csv
from crystal_emd.cluster_adress_func import cluster_list
clusterlistdf=cluster_list(os.path.dirname(nnadress))

for i,data in clusterlistdf.iterrows():
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    remake_csv(clusteradress,clusteradress)

clusterlistdf=cluster_list(os.path.dirname(nnadress))
for i,data in clusterlistdf.iterrows():
    clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
    make_cluster_dataset(cluster_adress=clusteradress,outdir=data.adress)