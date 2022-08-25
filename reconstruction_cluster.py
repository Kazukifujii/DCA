from cmath import nan
import numpy as np
import copy
import numpy as np
from constant import cluster_name
import pandas as pd
def first_cycle_func(isite,nn_data):
    #print(isite,nnlist)
    cycle_data = [coords for coords in nn_data[isite][1::]]
    return cycle_data

def search_index(isite,front_isite,nn_data):
    isite_list=[i[0] for i in nn_data[front_isite]]
    return isite_list.index(isite)

def read_info(isite,nn_data):
	first_info=[isite,nn_data[isite][0][0]]
	for i in nn_data[isite][0][-3::]:
		first_info.append(i)
	return first_info


def recoords(isite,nn_data_,adjacent_number=2,adj_j=1,clusterdf=nan):
	nn_data=copy.deepcopy(nn_data_)
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





"""
result_dir='/home/fujikazuki/crystal_emd/result/zeorite_4'
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
		cluster_2=create_neighbor_coords(isite,2,nn_data)
		print(cluster_2)
		sys.exit()

"""