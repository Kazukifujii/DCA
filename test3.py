import os
import re
import sys
import copy
import pickle
import argparse
import subprocess
import numpy as np


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


def first_cycle_func(isite,combination_data):
	#print(isite,nnlist)
	combination_data_ = copy.deepcopy(combination_data)
	cycle_data = []
	for i in combination_data_:
		if isite in i:
			i.remove(isite)
			cycle_data.append(i[0])
	return cycle_data



def n_cycle_func(isite,front_isite,combination_data):
	#print(isite,nnlist)
	combination_data_ = copy.deepcopy(combination_data)
	cycle_data = []
	for i in combination_data_:
		if isite in i:
			i.remove(isite)
			cycle_data.append(i[0])
	cycle_data.remove(front_isite)
	return cycle_data



def create_neighbor(adjacent_number,nn_data,combination_data):
	neighbor = {}
	for i in nn_data.keys():
		for j in range(1,int(adjacent_number)+1):
			save = []
			if j == 1:
				first_NN = first_cycle_func(i,combination_data)
				neighbor[i] = {1:[first_NN]}
			else:
				if j == 2:
					front_isite = [i]*len(neighbor[i][j-1][0])
				else:
					front_isite = []
					front_front_save = []
					for k in neighbor[i][j-2]:
						for l in k:
							front_front_save.append(l)
					for num,k in enumerate(neighbor[i][j-1]):
						for l in k:
							front_isite.append(front_front_save[num])
					
				neighbor[i][j] = []
				for k in neighbor[i][j-1]:
					for l in k:
						save.append(l)
				for num,k in enumerate(save):
					neighbor[i][j].append(n_cycle_func(k,front_isite[num],combination_data))

	return neighbor


def main():
	cwd = os.getcwd()

	parser = argparse.ArgumentParser()
	parser.add_argument('-nn','--adjacent_number', default=2)
	parser.add_argument('--output1', default='result')
	parser.add_argument('--output2', default='cod')
	parser.add_argument('-e','--explanation', default=False)
	args = parser.parse_args()

	if args.explanation:
		print('''cifdir : ['result/cod', 'result/cod/1000007', 'result/cod/1000017',...''')
		print('''neighbor : {1: [[21, 29, 30, 22, 31, 28]], 2: [[0, 9], [1, 4, 13], [1, 4, 14],...''')
		
		
		
		print('''combination_data : [[0, 24], [0, 21], [0, 28], [0, 31], [0, 22],... ''')
		print('''isite_data_list : ['Ca1', -1.07652858, 6.22898225, 3.78771229]''')
		print('''''')
		sys.exit()
	


	cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(args.output1 + "/" + args.output2))
	cifdir = cifdir_.split('\n')
	del cifdir[0]


	for i in cifdir:
		#cifnum = re.findall('\/(\w+)',i)[0]
		cifnum=os.path.basename(i)
		
		cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(i))
		with open(cifdir_nn_i_data,"rb") as frb:
			nn_data = pickle.load(frb)
			
		combination_data = create_combination(nn_data)
		neighbor_data = create_neighbor(args.adjacent_number,nn_data,combination_data)
		
		print(cifnum)
		with open(("{0}" + "/" + "neighbor_data_{1}.pickle").format(i,cifnum),"wb") as fwb:
	   		pickle.dump(neighbor_data,fwb)


if __name__ == '__main__':
	main()

