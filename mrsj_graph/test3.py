from crystal_emd.show import double_clusterplot,change

from glob import glob 
import pandas as pd
adress1='result/sort_volume_ciffiles_top_100/8000163/8000163_13_0.csv'
adress2='result/allzeorite/CZP/CZP_9_11.csv'
df=pd.read_csv(adress1,index_col=0)
df2=pd.read_csv(adress2,index_col=0)
from crystal_emd.read_info import clusterplot
#clusterplot(df2,show=True,save=False)
change(adress2,adress1,show=True,save=False)

'''
from crystal_emd.read_info import Set_Cluster_Info
import pickle
nn_data=pickle.load(open('result/testcif_n=4/ABW/nb_ABW.pickle','rb'))
from crystal_emd.show import clusterplot
color={'Si1':'blue','O1':'red'}
import matplotlib.pyplot as plt
for isite in range(3):
    cluster=Set_Cluster_Info(nn_data=nn_data,adjacent_number=2,isite=isite)
    cluster.parallel_shift_of_center()
    clusterplot(clusterdf=cluster.cluster_coords,color=color,text=False)
    plt.legend()
    plt.title('ABW_cluster_isite={}'.format(isite))
    plt.savefig('ABW_cluster_isite={}.png'.format(isite))
    plt.close()


'''