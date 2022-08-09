import os,pickle,re,sys
import subprocess
import collections
import numpy as np

def flatten(l):
	#https://note.nkmk.me/python-list-flatten/
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def all_cordinate_info(isite,nn_data,neighbor_data):
	all_adjacent_isite=[i for i in flatten(list(neighbor_data.values()))]
	all_adjacent_coordinate_=list()
	for i_site in all_adjacent_isite:
		all_adjacent_coordinate_.append(nn_data[i_site][0][-3::])
	return np.array(all_adjacent_coordinate_)

def find_xz_shaft(isite,nn_data):
	lenge=[]
	center_c=nn_data[isite][0][-3::]
	for i in nn_data[isite][1::]:
		ic=i[-3::]
		i_site=i[0]
		ilenge=np.linalg.norm(np.array(ic)-np.array(center_c))
		lenge.append((ilenge,i_site))
	lenge.sort(key=lambda x:x[0])
	print(lenge)
	print(nn_data[isite])
	print(center_c,nn_data[lenge[0][1]][0][-3::],nn_data[lenge[0][1]][1][-3::])
	return center_c,nn_data[lenge[0][1]][0][-3::],nn_data[lenge[0][1]][1][-3::]

class Set_Cluster_Info:
	def __init__(self,isite,nn_data,neighbor_data):
		#_c:_cordinate
		self.isite=isite
		self.nn_data=nn_data
		self.neighbor_data=neighbor_data
		self.all_adjacent_c=all_cordinate_info(isite,nn_data,neighbor_data)
		self.center_c,self.main_shaft_c,self.sub_shaft_c=find_xz_shaft(isite,nn_data)
		

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
		cluster_1=Set_Cluster_Info(isite,nn_data,neighbor_data[isite])
		sys.exit()
