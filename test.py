from crystal_emd.read_info import recoords,clusterplot,Set_Cluster_Info
import pickle

f=pickle.load(open('result/testcif/ABW/nb_ABW.pickle','rb'))
import pandas as pd
clusterdf=pd.read_csv('result/testcif/ABW/ABW_0_0.csv',index_col=0)

df=Set_Cluster_Info(clusterdf=clusterdf)

clusterplot(clusterdf=df.cluster_coords,show=True,save=False)