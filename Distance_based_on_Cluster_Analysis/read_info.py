import numpy as np
import pandas as pd
from cmath import nan
import copy,re,itertools
from .constant import cluster_name
from copy import deepcopy
import subprocess
import re
from math import isclose


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
	
	if adj_j==1:
		firstdata=[[0]+center_info(isite,nn_data)+[nan]]
		for i in first_cycle_func(isite,nn_data):
			firstdata.append([1]+i+[0])
		clusterdf=pd.DataFrame(firstdata,columns=cluster_name)
	if adj_j==adjacent_number:
		return clusterdf
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
	neighbor_num_=coords.neighbor_num.to_list()
	neighbor_num_.sort()
	neighbor_num_=neighbor_num_[1]
	shaftdata=coords[coords.neighbor_num==neighbor_num_].iloc[:,1:-1].values.tolist()
	combinations=list(itertools.combinations(shaftdata,2))
	return copy.deepcopy(combinations)


def shaft_info(coords_):
	coords=copy.deepcopy(coords_)
	comb=list()
	center_c=coords.loc[0,'x':'z']
	for data in shaft_comb(coords):
		lenge=[]
		"""
		for shaft in data:
			ic=shaft[-3::]
			i_site=shaft[0]
			ilenge=np.linalg.norm(np.array(ic)-np.array(center_c))
			lenge.append((ilenge,i_site))
			lenge.sort(key=lambda x:x[0])
		main_c=coords[(coords.neighbor_num==1) & (coords.isite==lenge[0][1])].iloc[:,1:-1].values.tolist()[0]
		sub_c=coords[(coords.neighbor_num==1) & (coords.isite==lenge[1][1])].iloc[:,1:-1].values.tolist()[0]
		"""
		main_c,sub_c=data
		comb.append((main_c,sub_c))
		main_c2=copy.deepcopy(sub_c)
		sub_c2=copy.deepcopy(main_c)
		comb.append((main_c2,sub_c2))
	return comb

class Set_Cluster_Info():
	def __init__(self,isite=None,nn_data=None,adjacent_number=None,clusterdf=None):
		#_c:_coordinate
		if not clusterdf is None:
			self.cluster_coords=deepcopy(clusterdf)
			self.isite=self.cluster_coords.loc[0,'isite']
			self.shaft_comb=shaft_info(self.cluster_coords)
			self.orignal_cluster_coords=copy.deepcopy(self.cluster_coords)
			return
		self.nn_data=copy.deepcopy(nn_data)
		self.cluster_coords=recoords(isite,self.nn_data,adjacent_number)
		self.isite=isite
		self.shaft_comb=shaft_info(self.cluster_coords)
		self.orignal_cluster_coords=copy.deepcopy(self.cluster_coords)
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
		self.orignal_cluster_coords=copy.deepcopy(self.cluster_coords)

	def rotation(self,pattern=0):
		self.main_shaft_c,self.sub_shaft_c=self.shaft_comb[pattern]
		ra=self.main_shaft_c[-3::]
		rb=self.sub_shaft_c[-3::]
		#must run parallel_shift_of_center
		z1=np.linalg.norm(ra,ord=2)
		rot3=ra/z1
		z2=np.dot(rb,rot3)
		x2=np.linalg.norm(rb-z2*rot3)
		if isclose(x2,0,abs_tol=1e-8):
			rot1=[1,0,1]
		else:
			rot1=(rb-z2*rot3)/x2
		rot2=np.cross(rot3,rot1)
		rot_=np.array([rot1,rot2,rot3])
		self.rot=np.linalg.inv(rot_)
		for i,data in self.orignal_cluster_coords.loc[:,'x':'z'].iterrows():
			self.cluster_coords.loc[i,'x':'z']=data.dot(self.rot)


def remake_csv(csvn,outname=False,atom='Si1'):
    df=pd.read_csv(csvn,index_col=0)
    df2=df[df.atom=='Si1'].copy()
    for i,data in df[df.atom==atom].iterrows():
        if i==0:
            continue
        if df.loc[data.front_index].atom==atom:
            continue
        idx=df.loc[data.front_index].front_index
        df2.loc[i,'front_index']=deepcopy(idx)
    oldindexlist=df2.index.to_list()
    df2=df2.reset_index().copy()
    newindexlist=df2.index.to_list()
    numdict=dict()
    for i,number in enumerate(oldindexlist):
        numdict[number]=newindexlist[i]
    df2.loc[:,'front_index']=df2.front_index.replace(numdict).copy()
    csvname=re.split('/',csvn)[-1]
    dir=csvn.replace(csvname,'')
    if outname:
        df2.to_csv(outname)
    else:
        df2.to_csv('{}{}_{}'.format(dir,atom,csvname))
    return df2


def reconstruction_branch(clusterdf,indexnum,initial=pd.DataFrame()):
    result=deepcopy(initial)
    if (clusterdf.front_index==indexnum).sum()==0:
        return result
    for i,data in clusterdf[clusterdf.front_index==indexnum].iterrows():
        result=pd.concat([result,data],axis=1)
        result=reconstruction_branch(clusterdf,i,result)
    return result


def cluster_branch(clusterdf):
	"""
	from Distance_based_on_Cluster_Analysis.read_info import cluster_branch
	df=pd.read_csv('test.csv',index_col=0)
	a=cluster_branch(df)
	print(a)
	"""
	branch=list()
	centerdf=clusterdf.iloc[0].copy()
	for i,data in clusterdf[clusterdf.front_index==0].iterrows():
		branchdf=pd.concat([reconstruction_branch(clusterdf=clusterdf,indexnum=i,initial=data),centerdf],axis=1).T.copy().sort_values(by='neighbor_num')
		numericcolumns=['neighbor_num','isite','x','y','z','front_index']
		branchdf[numericcolumns]=branchdf[numericcolumns].astype(float)
		branch.append(branchdf)
	return branch

def make_sort_ciffile(dir,estimecont=2000):
    cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(dir))
    cifdir = cifdir_.split('\n')
    del cifdir[0]
    isiteinfo=list()
    for i in cifdir:
        cifid=re.split('/',i)[-1]
        lasttxt=subprocess.getoutput("grep ' Si' {}/{}.txt |tail -n 1".format(i,cifid))
        try:
            maxisite=int(re.split('Si',lasttxt)[0].replace(' ',''))
        except:
            continue
        isiteinfo.append((cifid,i,maxisite))
    isiteinfo.sort(key=lambda x:x[-1])
    if estimecont=='all':
        info=pd.DataFrame(isiteinfo,columns=['cifid','cifadress','Si_len'])
        info.to_csv('{}/picupadress'.format(dir))
        print(info.Si_len.sum())
        return info
    cont=0
    picupadress=list()
    for i in isiteinfo:
        cont+=i[-1]
        picupadress.append(i)
        if cont>=estimecont:
            break
        continue
    print(cont)
    info=pd.DataFrame(picupadress,columns=['cifid','cifadress','Si_len'])
    info.to_csv('{}/picupadress'.format(dir))
    return info


from .connection_func import IterativeClosestPoint as icp
def cluster_match(clusterdf1,clusterdf2,convergence_val=10**(-8)):
    a=cluster_branch(clusterdf1)
    b=cluster_branch(clusterdf2)
    fmachnum=list()
    for i,ai in enumerate(a):
        for j,bi in enumerate(b):
            if j in fmachnum:
                continue
            branch_matching=icp(ai,bi)
            mcheck=branch_matching.start_cal(convergence_val=convergence_val)
            if mcheck:
                fmachnum.append(j)
                break
    if len(fmachnum)==len(a):
        return True
    return False


def Si_distance(csv):
    df=pd.read_csv(csv,index_col=0)
    branch=cluster_branch(df)
    alist=[]
    blist=[]
    for i in branch:
        xi=i['x'].iloc[2]
        yi=i['y'].iloc[2]
        zi=i['z'].iloc[2]
        a=(xi**2+yi**2+zi**2)**0.5
        alist.append(a)
    for j in itertools.product(branch, repeat=2):
        xj=j[0]['x'].iloc[2]-j[1]['x'].iloc[2]
        yj=j[0]['y'].iloc[2]-j[1]['y'].iloc[2]
        zj=j[0]['z'].iloc[2]-j[1]['z'].iloc[2]
        b=(xj**2+yj**2+zj**2)**0.5
        blist.append(b)
    
    alist.extend(blist)
    ablist=alist
    columns=['ai', 'b0i','b1i','b2i','b3i']
    df2 = pd.DataFrame()
    for i in range(len(branch)+1):
        df2[columns[i]] = ablist[i*len(branch):(i+1)*len(branch)]
    return(df2)