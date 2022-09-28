import numpy as np
import pandas as pd
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt
from cmath import nan
import copy,re,itertools
from .constant import cluster_name


def first_cycle_func(isite,nn_data):
    #print(isite,nnlist)
    cycle_data = [coords for coords in nn_data[isite][1::]]
    return cycle_data

def search_index(isite,front_isite,nn_data):
    isite_list=[i[0] for i in nn_data[front_isite]]
    return isite_list.index(isite)

def center_info(isite,nn_data):
	first_info=[isite,nn_data[isite][0][0]]
	for i in nn_data[isite][0][-3::]:
		first_info.append(i)
	return first_info

def recoords(isite,nn_data_,adjacent_number=2,adj_j=1,clusterdf=nan):
	nn_data=copy.deepcopy(nn_data_)
	if adj_j==adjacent_number:
		return clusterdf
	if adj_j==1:
		firstdata=[[0]+center_info(isite,nn_data)+[nan]]
		for i in first_cycle_func(isite,nn_data):
			firstdata.append([1]+i+[0])
		clusterdf=pd.DataFrame(firstdata,columns=cluster_name)
	neigbordata=[]
	for num,idata in clusterdf.loc[clusterdf['neighbor_num']==adj_j].iterrows():
		front_index=clusterdf.loc[idata.front_index].isite
		rjc=nn_data[idata.isite][0][-3::]
		rijn=idata.loc['x':'z']
		difrij=rjc-rijn
		for jdata_ in nn_data[idata.isite][1::]:
			jdata=copy.deepcopy(jdata_)
			if jdata[0]==front_index:
				continue
			rjkn=jdata[-3::]
			rkc=rjkn-difrij
			jdata[-3::]=rkc
			neigbordata.append([adj_j+1]+jdata+[num])
	clusterdf_=pd.DataFrame(neigbordata,columns=cluster_name)
	clusterdf=pd.concat([clusterdf,clusterdf_],ignore_index=True)
	return recoords(isite,nn_data,adjacent_number,adj_j+1,clusterdf)

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
	
def read_nood(clusterdf):
	noods=list()
	for index,i in clusterdf.iterrows():
		if index==0:
			continue
		front_idx=i.loc['front_index']
		a=clusterdf.loc[front_idx].loc['x':'z']
		b=i.loc['x':'z']
		bondx=[a.x,b.x]
		bondy=[a.y,b.y]
		bondz=[a.z,b.z]
		bondx.sort()
		bondy.sort()
		bondz.sort()
		noods.append((bondx,bondy,bondz))
	return noods
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

def remake_csv(csvn,outname=True,atom='Si1'):
    df=pd.read_csv(csvn,index_col=0)
    from copy import deepcopy
    df2=df[df.atom=='Si1'].copy()
    for i,data in df[df.atom==atom].iterrows():
        if i==0:
            continue
        idx=df.loc[data.front_index].front_index
        df2.loc[i,'front_index']=deepcopy(idx)
    oldindexlist=df2.index.to_list()
    df2=df2.reset_index().copy()
    newindexlist=df2.index.to_list()
    numdict=dict()
    for i,number in enumerate(oldindexlist):
        numdict[number]=newindexlist[i]
    df2=df2.replace(numdict).copy()
    csvname=re.split('/',csvn)[-1]
    dir=csvn.replace(csvname,'')
    if not type(outname) is str:
        df2.to_csv('{}{}_{}'.format(dir,atom,csvname))
    else:
        df2.to_csv(outname)
    return df2