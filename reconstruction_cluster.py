import itertools
from operator import ne
import os
import re
import sys
import pickle
import subprocess
import numpy as np
import os
import re
import sys
import copy
import pickle
import subprocess
import numpy as np

def read_info(isiet,nn_data):
	first_info=[isite,nn_data[isiet][0][0]]
	for i in nn_data[isiet][0][-3::]:
		first_info.append(i)
	return [first_info]

def create_combination(nn_data):
	combination_data_ = []
	for i in nn_data.keys():
		for num,j in enumerate(nn_data[i]):
			if not num == 0:
				nnbond = [i,j[0]]
				nnbond.sort()
				combination_data_.append(nnbond)
	combination_data__ = []
	combination_data = [x for x in combination_data_ if x not in combination_data__ and not combination_data__.append(x)]
	#print(combination_data)
	
	return combination_data


def first_cycle_func(isite,nn_data,combination_data):
    #print(isite,nnlist)
    combination_data_ = copy.deepcopy(combination_data)
    cycle_data = []
    for i in combination_data_:
        if isite in i:
            i.remove(isite)
            cycle_data.append(i[0])
    cycle_data = [coords for coords in nn_data[isite][1::]]
    return cycle_data

def search_index(isite,front_isite,nn_data):
    isite_list=[i[0] for i in nn_data[front_isite]]
    return isite_list.index(isite)

def recluclate_coords(isite,front_isite,cycle_data,nn_data):
    ric = np.array(nn_data[isite][0][-3::])
    idx=search_index(isite,front_isite,nn_data)
    rnij = np.array(nn_data[front_isite][idx][-3::])
    coords=[]
    for i in cycle_data:
        rdij = ric-rnij
        idx=search_index(i,isite,nn_data)
        k=nn_data[isite][idx].copy()
        rkjn=np.array(k[-3::])
        rnijk=rkjn-rdij
        k[-3],k[-2],k[-1]=rnijk[0],rnijk[1],rnijk[2]
        coords.append(k)
    return coords

def n_cycle_func(isite,nn_data,front_isite,combination_data):
    combination_data_ = copy.deepcopy(combination_data)
    cycle_data = []
    for i in combination_data_:
        if isite in i:
            i.remove(isite)
            cycle_data.append(i[0])
    cycle_data.remove(front_isite)
    cycle_coords=recluclate_coords(isite,front_isite,cycle_data,nn_data)
    return cycle_coords

def create_neighbor_coords(isite,adjacent_number,nn_data):
    combination_data = create_combination(nn_data)
    neighbor = {0:read_info(isite,nn_data)}
    i=isite
    for j in range(1,int(adjacent_number)+1):
        save = []
        if j == 1:
            first_NN = first_cycle_func(i,nn_data,combination_data)
            neighbor[j] = [first_NN]
        else:
            if j == 2:
                front_isite = [i]*len(neighbor[j-1][0])
            else:
                front_isite = []
                front_front_save = []
                for k in neighbor[j-2]:
                    for l in k:
                        front_front_save.append(l[0])
                for num,k in enumerate(neighbor[j-1]):
                    for l in k:
                        front_isite.append(front_front_save[num])
            neighbor[j] = []
            for k in neighbor[j-1]:
                for l in k:
                    save.append(l[0])
            for num,k in enumerate(save):
                neighbor[j].append(n_cycle_func(k,nn_data,front_isite[num],combination_data))
    return neighbor


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

