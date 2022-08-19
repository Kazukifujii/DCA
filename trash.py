
from operator import ne
from tkinter.tix import Tree
import numpy as np
import itertools

def remake_cluster_coords(isite,nn_data,neighbor_data,cluster_coords=dict(),adjacentnum=1):
	#Calculate the coordinates of the second and subsequent neighbors
	if not adjacentnum+1 in neighbor_data:
		print('non')
		return cluster_coords
	if not any(cluster_coords):
		cluster_coords[isite]=nn_data[isite][0][-3::]
		cluster_coords_=[]
		for nn_data_i in nn_data[isite][1::]:
			cluster_coords_.append(nn_data_i[-3::])
		cluster_coords[adjacentnum]=cluster_coords_
	#for i in neighbor_data[]
	j=isite
	i_nsite=list(itertools.chain.from_iterable(neighbor_data[adjacentnum-1]))
	for ki,k_nsite in enumerate(neighbor_data[adjacentnum]):
		i=i_nsite[ki]
		for k in k_nsite:
			index=[x[0] for x in nn_data[j][1::]].index(i)
			rdij=np.array(cluster_coords[adjacentnum-1])-np.array(nn_data[j][index][-3::])
			rk=np.array(nn_data[k][0][-3::])-rdij
	cluster_coords=remake_cluster_coords(i,nn_data,neighbor_data,adjacentnum=adjacentnum+1)
	return cluster_coords

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

from constant import cluster_name
from reconstruction_cluster import first_cycle_func,read_info
import pandas as pd
import copy
def recoords(isite,nn_data,adjacent_number=2,adj_j=1,clusterdf=nan):
	if adj_j==adjacent_number:
		return clusterdf
	if adj_j==1:
		firstdata=[[0]+read_info(isite,nn_data)+[nan]]
		for i in first_cycle_func(isite,nn_data):
			firstdata.append([1]+i+[0])
		clusterdf=pd.DataFrame(firstdata,columns=cluster_name)
	
	neigbordata=[]
	for num,idata in clusterdf.loc[clusterdf['neighbor_num']==adj_j].iterrows():
		front_index=clusterdf.loc[idata.front_index].isite
		rjc=nn_data[idata.isite][0][-3::]
		rijn=idata.loc['x':'z']
		difrij=rjc-rijn
		if num==6 or num==8:
			print(rjc,rijn.to_list())
			print(difrij)
		for jdata in nn_data[idata.isite][1::]:
			if jdata[0]==front_index:
				continue
			jdata_=copy.copy(jdata)
			rjkn=jdata_[-3::]
			rkc=rjkn-difrij
			jdata_[-3::]=rkc
			neigbordata.append([adj_j+1]+jdata_+[num])
	clusterdf_=pd.DataFrame(neigbordata,columns=cluster_name)
	clusterdf=pd.concat([clusterdf,clusterdf_],ignore_index=True)
	return recoords(isite,nn_data,adjacent_number,adj_j+1,clusterdf)
	
clusterdf=recoords(0,nn_data,adjacent_number=3)
from read_info import clusterplot as clp

clp(clusterdf)