from crystal_emd.show import change
import pandas as pd

adress1='result/sort_volume_ciffiles_top_100/8000163/8000163_13_0.csv'
adress2='result/allzeorite/CZP/CZP_9_11.csv'

df=pd.read_csv(adress1,index_col=0)
df2=pd.read_csv(adress2,index_col=0)
change(adress2,adress1,show=False,text=False,save=True)

'''
from crystal_emd.read_info import Set_Cluster_Info
color={'Si1':'blue','O1':'red'}
import matplotlib.pyplot as plt
from crystal_emd.show import clusterplot
cluster=Set_Cluster_Info(clusterdf=pd.read_csv(adress1,index_col=0)) 
clusterplot(clusterdf=cluster.cluster_coords,color=color,text=False)
plt.legend()
plt.title('8000163_13')
plt.savefig('8000163_cluster_isite=13.svg')
plt.close()
'''