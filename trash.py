
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from plotly.graph_objs import Scatter
from plotly.offline import init_notebook_mode, iplot


def clusterplotly(clusterdf,title='cluster.png'):
	noods=list()
	for index,i in clusterdf.iterrows():
		if index==0:
			continue
		front_idx=i.loc['front_index']
		a=clusterdf.loc[front_idx].loc['x':'z']
		b=i.loc['x':'z']
		noods.append(([a.x,b.x],[a.y,b.y],[a.z,b.z]))
	import plotly.express as px
	fig=px.scatter_3d(clusterdf,x='x',y='y',z='z',size_max=5)
	
	fig.show()

import os,pickle
import subprocess
from read_info import Set_Cluster_Info
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


import re
if not os.path.isdir('testdir'):
	os.mkdir('testdir')
os.chdir('testdir')
for isite in nn_data.keys():
	isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
	if isite_atom == 'Si':
		cluster_1=Set_Cluster_Info(isite,nn_data,4)
		cluster_1.cluster_coords.to_csv('cluster_%d.csv'%isite)
		cluster_1.parallel_shift_of_center()
		cluster_1.rotation()
		clusterplotly(cluster_1.cluster_coords,title='cluster%d.png'%isite)
		import sys
		sys.exit()
	
	
	
	
	