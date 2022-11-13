i='cluster_dataset/CHA'
import os
cifid=os.path.basename(i)
print(cifid)


cont=0
import pandas as pd
from crystal_emd.read_info import Set_Cluster_Info
cwd=os.getcwd()
from crystal_emd.cluster_adress_func import cluster_list
clusterlist=cluster_list(i)
alllen_=clusterlist.index.to_list()[-1]+1
os.chdir(i)
for i,data in clusterlist.iterrows():
    csvadress='{}_{}_0.csv'.format(data.cifid,data.isite)
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
print()
