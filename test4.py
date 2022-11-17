from crystal_emd.read_info import Set_Cluster_Info
import pickle

nn_data=pickle.load(open('result/randzeo/ID302/ID302.randzeo.pickle','rb'))
#info=Set_Cluster_Info(nn_data=nn_data,isite=1,adjacent_number=4)
from crystal_emd.read_info import clusterplot
from crystal_emd.show import change
from glob import glob
adress1='{}/{}_{}_{}.csv'.format('database','CHI',24,3)
adress2='{}/{}_{}_{}.csv'.format('result/randzeo/ID302','ID302',1,0)
change(adress1, adress2)
#clusterplot(info.cluster_coords,show=True,save=False)
