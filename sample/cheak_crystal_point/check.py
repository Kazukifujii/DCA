import pandas as pd

cifpointdf=pd.read_csv('result/allzeorite/cifpoint')
from crystal_emd.cluster_adress_func import cluster_list

datasetlist=cluster_list('cluster_dataset',dirs=True)
datasetlist=datasetlist.cifid.drop_duplicates().to_list()


for i,data in cifpointdf.iterrows():
    cheak_dataset=data.cifid in datasetlist
    cifpointdf.loc[i,'dataset']=cheak_dataset

print(cifpointdf)