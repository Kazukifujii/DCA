from cmath import nan
import os,pickle
import subprocess
from read_info import Set_Cluster_Info
from read_info import clusterplot
result_dir='/home/fujikazuki/crystal_emd/result/cod'
atom='Si'
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(result_dir))
cifdir = cifdir_.split('\n')
del cifdir[0]
cifnum=os.path.basename(result_dir)
#read nn_data
cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(cifdir[0]))
with open(cifdir_nn_i_data,"rb") as frb:
	nn_data = pickle.load(frb)
#read neighbor_data
cifdir_neighbor_i_data = subprocess.getoutput("find {0} -name neighbor_data_*.pickle".format(cifdir[0]))
with open(cifdir_neighbor_i_data,"rb") as frb:
	neighbor_data = pickle.load(frb)


from read_info import clusterplot as clp
import re
for isite in nn_data.keys():
	isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
	if isite_atom == 'Si':
		cluster_1=Set_Cluster_Info(isite,nn_data,4)
		cluster_1.cluster_coords.to_csv('cluster_%d.csv'.format(isite))
		cluster_1.parallel_shift_of_center()
		cluster_1.rotation()
		clp(cluster_1.cluster_coords,title='cluster%d.png'%isite)
