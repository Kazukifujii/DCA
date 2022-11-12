from crystal_emd.read_info import recoords,clusterplot,Set_Cluster_Info
import pickle

f=pickle.load(open('result/testcif/ABW/nb_ABW.pickle','rb'))
info=Set_Cluster_Info(1,nn_data_=f,adjacent_number=1)
info.parallel_shift_of_center()
info.rotation(pattern=0)
print('end rot')
clusterplot(info.cluster_coords,show=True,save=False)