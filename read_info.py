import copy
import numpy as np
from reconstruction_cluster import recoords
import pandas as pd
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt
import itertools

cul_name=['neighbor_num','isite','atom','x','y','z','front_index']

def shaft_comb(coords):
	#print(coords.head(5))
	shaftdata=coords[coords.neighbor_num==1].iloc[:,1:-1].values.tolist()
	combinations=list(itertools.combinations(shaftdata,2))
	return copy.deepcopy(combinations)


def shaft_info(coords_):
	coords=copy.deepcopy(coords_)
	comb=list()
	center_c=coords.loc[0,'x':'z']
	for data in shaft_comb(coords):
		lenge=[]
		for shaft in data:
			ic=shaft[-3::]
			i_site=shaft[0]
			ilenge=np.linalg.norm(np.array(ic)-np.array(center_c))
			lenge.append((ilenge,i_site))
			lenge.sort(key=lambda x:x[0])
		main_c=coords[(coords.neighbor_num==1) & (coords.isite==lenge[0][1])].iloc[:,1:-1].values.tolist()[0]
		sub_c=coords[(coords.neighbor_num==1) & (coords.isite==lenge[1][1])].iloc[:,1:-1].values.tolist()[0]
		comb.append((main_c,sub_c))
		main_c2=copy.deepcopy(sub_c)
		sub_c2=copy.deepcopy(main_c)
		comb.append((main_c2,sub_c2))
	return comb

class Set_Cluster_Info():
	def __init__(self,isite,nn_data_,adjacent_number=2):
		#_c:_coordinate
		self.nn_data=copy.deepcopy(nn_data_)
		self.cluster_coords=recoords(isite,self.nn_data,adjacent_number)
		self.isite=isite
		self.shaft_comb=shaft_info(self.cluster_coords)

	def parallel_shift_of_center(self,coords=[0,0,0]):
		dif_coords=np.array(coords)-self.cluster_coords.loc[0].loc['x':'z'].to_list()
		difdf=pd.DataFrame(columns=['x','y','z'],index=self.cluster_coords.index.to_list())
		difdf.x=dif_coords[0]
		difdf.y=dif_coords[1]
		difdf.z=dif_coords[2]
		self.cluster_coords.x=self.cluster_coords.x+difdf.x
		self.cluster_coords.y=self.cluster_coords.y+difdf.y
		self.cluster_coords.z=self.cluster_coords.z+difdf.z
		self.shaft_comb=shaft_info(self.cluster_coords)	

	def rotation(self,pattern=0):
		self.main_shaft_c,self.sub_shaft_c=self.shaft_comb[pattern]
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
		self.rot_cluster_coords=copy.deepcopy(self.cluster_coords)
		for i,data in self.cluster_coords.loc[:,'x':'z'].iterrows():
			self.cluster_coords.loc[i,'x':'z']=data.dot(self.rot)
	

def clusterplot(clusterdf,title='cluster.png',show=None,save=True):
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
	ax.set_xlim(-5,5)
	ax.set_ylim(-5,5)
	ax.set_zlim(-5,5)
	ax.scatter(clusterdf.x,clusterdf.y,clusterdf.z)
	for index,i in clusterdf.iterrows():
		text=i.atom+'_'+str(i.isite)
		ax.text(i.x,i.y,i.z,text)
	for nood in noods:
		line = art3d.Line3D(*nood)
		ax.add_line(line)
	fig.suptitle(title)
	if save:
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