
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
