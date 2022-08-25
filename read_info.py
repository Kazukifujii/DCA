import copy
import numpy as np
from reconstruction_cluster import recoords
import pandas as pd
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt



cul_name=['neighbor_num','isite','atom','x','y','z','front_index']


def find_xz_shaft(isite,nn_data):
	lenge=[]
	center_c=nn_data[isite][0][-3::]
	for i in nn_data[isite][1::]:
		ic=i[-3::]
		i_site=i[0]
		ilenge=np.linalg.norm(np.array(ic)-np.array(center_c))
		lenge.append((ilenge,i_site))
	lenge.sort(key=lambda x:x[0])
	from reconstruction_cluster import search_index
	main_idx=search_index(lenge[0][1],isite,nn_data)
	sub_idx=search_index(lenge[1][1],isite,nn_data)
	return nn_data[isite][main_idx],nn_data[isite][sub_idx]

class Set_Cluster_Info():
	def __init__(self,isite,nn_data_,adjacent_number=2):
		#_c:_coordinate
		self.nn_data=copy.deepcopy(nn_data_)
		self.cluster_coords=recoords(isite,self.nn_data,adjacent_number)
		self.isite=isite
		self.main_shaft_c,self.sub_shaft_c=find_xz_shaft(isite,self.nn_data)

	def parallel_shift_of_center(self,coords=[0,0,0]):
		dif_coords=np.array(coords)-self.cluster_coords.loc[0].loc['x':'z'].to_list()
		difdf=pd.DataFrame(columns=['x','y','z'],index=self.cluster_coords.index.to_list())
		difdf.x=dif_coords[0]
		difdf.y=dif_coords[1]
		difdf.z=dif_coords[2]
		self.main_shaft_c[-3::]=self.main_shaft_c[-3::]+dif_coords
		self.sub_shaft_c[-3::]=self.sub_shaft_c[-3::]+dif_coords
		self.cluster_coords.x=self.cluster_coords.x+difdf.x
		self.cluster_coords.y=self.cluster_coords.y+difdf.y
		self.cluster_coords.z=self.cluster_coords.z+difdf.z

	def rotation(self):
		ra=self.main_shaft_c[-3::]
		rb=self.sub_shaft_c[-3::]
		#must run parallel_shift_of_center
		z1=np.linalg.norm(ra,ord=2)
		rot3=ra/z1
		z2=np.dot(rb,rot3)
		x2=np.linalg.norm(rb-z2*rot3)
		rot1=(rb-z2*rot3)/x2
		rot2=np.cross(rot3,rot1)
		rot_=np.array([rot1,rot2,rot3])
		self.rot=np.linalg.inv(rot_)
		for i,data in self.cluster_coords.loc[:,'x':'z'].iterrows():
			self.cluster_coords.loc[i,'x':'z']=data.dot(self.rot)
	

def clusterplot(clusterdf,title='cluster.png',show=None):
	noods=list()
	for index,i in clusterdf.iterrows():
		if index==0:
			continue
		front_idx=i.loc['front_index']
		a=clusterdf.loc[front_idx].loc['x':'z']
		b=i.loc['x':'z']
		noods.append(([a.x,b.x],[a.y,b.y],[a.z,b.z]))
	fig = plt.figure(figsize = (12, 12))
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(clusterdf.x,clusterdf.y,clusterdf.z)
	for index,i in clusterdf.iterrows():
		text=i.atom+'_'+str(i.isite)
		ax.text(i.x,i.y,i.z,text)
	for nood in noods:
		line = art3d.Line3D(*nood)
		ax.add_line(line)
	fig.savefig(title)
	if show:
		plt.show()
	plt.close()
	

"""
import os,pickle,re,sys
import subprocess
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

#filterling by atom
for isite in nn_data.keys():
	isite_atom = re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
	if isite_atom == atom:
		cluster_1=Set_Cluster_Info(isite,nn_data,3)
		cluster_1.parallel_shift_of_center()
		sys.exit()
"""