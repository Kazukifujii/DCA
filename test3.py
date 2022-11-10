from glob import glob as gl
import random,sys
from crystal_emd.cluster_pointing import make_cluster_point
datasetadress='result/allzeorite'
#sample_cluster=random.sample(clusterlist,100)


import pandas as pd
d=pd.read_csv('result/allzeorite/picupadress',index_col=0)
sample_cluster=d[d.Si_len<=15].cifadress.to_list()
print(sample_cluster)
sys.exit()
d=make_cluster_point(datasetadress=datasetadress)

for i in sample_cluster:
    d=make_cluster_point(datasetadress=datasetadress)
    d.point(i, n_job=-1)
    

