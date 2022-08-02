import os
import re
import sys
import pickle
import argparse
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d

def cre_plotdata(isite,nn_data,neighbor_data,cifnum):
	
	fig = plt.figure(figsize = (12, 12))
	ax = fig.add_subplot(111, projection='3d')
	ax.set_title("ce_fraction = "+str(nn_data[isite][0][1]))

	# original
	otag,ox,oy,oz = nn_data[isite][0][0]+'_'+str(isite),nn_data[isite][0][2],nn_data[isite][0][3],nn_data[isite][0][4]
	#print(otag)
	#if otag == 'Ca0.015_174':
	
	first_neighbor = []
	second_neighbor = []
	for i in nn_data[isite][1::]:
		# plot first neighbor
		ax.scatter(i[2],i[3],i[4],color='r')
		ax.text(i[2],i[3],i[4],i[1]+'_'+str(i[0]))
		# original - first neighbor
		line = art3d.Line3D([ox,i[2]],[oy,i[3]],[oz,i[4]], color='y')
		ax.add_line(line)
	
		second_neighbor_ = []
		if i[0] in nn_data:
			diffx,diffy,diffz = nn_data[i[0]][0][2]-i[2],nn_data[i[0]][0][3]-i[3],nn_data[i[0]][0][4]-i[4]
			for j in nn_data[i[0]][1::]:
				#print(j[0],first_neighbor)
				if not j[0] in first_neighbor:
					second_neighbor_.append(j[0])
					# plot second neighbor
					secondtag,secondox,secondoy,secondoz = j[1]+'_'+str(j[0]),j[2],j[3],j[4]
					secondx,secondy,secondz = j[2]-diffx,j[3]-diffy,j[4]-diffz
					ax.scatter(secondx,secondy,secondz,color='g')
					ax.text(secondx,secondy,secondz,secondtag)
					# first neighbor - second neighbor
					line = art3d.Line3D([i[2],secondx],[i[3],secondy],[i[4],secondz], color='y')
					ax.add_line(line)
					
		
		first_neighbor.append(i[0])
		second_neighbor.append(second_neighbor_)
	
	"""
	#print(nn_data[0])
	print(neighbor_data)
	print(first_neighbor)
	print(len(set(neighbor_data[1][0])-set(first_neighbor)))
	print(second_neighbor)
	"""
	
	# from one side bond
	if len(set(neighbor_data[1][0])-set(first_neighbor)) != 0:
		for i in set(neighbor_data[1][0])-set(first_neighbor):
			for j in nn_data[i][1::]:
				if j[0] == isite:
					diffx,diffy,diffz = ox-j[2],oy-j[3],oz-j[4]
			# plot first neighbor
			firsttag,firstx,firsty,firstz = nn_data[i][0][0]+'_'+str(i),nn_data[i][0][2]+diffx,nn_data[i][0][3]+diffy,nn_data[i][0][4]+diffz
			ax.scatter(firstx,firsty,firstz,color='r')
			ax.text(firstx,firsty,firstz,firsttag)
			# original - first neighbor
			line = art3d.Line3D([ox,firstx],[oy,firsty],[oz,firstz], color='y')
			ax.add_line(line)
			
			second_neighbor2 = []
			if i in nn_data:
				diffx,diffy,diffz = firstx-nn_data[i][0][2],firsty-nn_data[i][0][3],firstz-nn_data[i][0][4]
				for j in nn_data[i][1::]:
					secondtag,secondx,secondy,secondz = j[1]+'_'+str(j[0]),j[2]+diffx,j[3]+diffy,j[4]+diffz
					# plot second neighbor
					ax.scatter(secondx,secondy,secondz,color='g')
					ax.text(secondx,secondy,secondz,secondtag)
					# first neighbor - second neighbor
					line = art3d.Line3D([firstx,secondx],[firsty,secondy],[firstz,secondz], color='y')
					ax.add_line(line)
					
					second_neighbor2.append(j[0])
					
			indexnum = neighbor_data[1][0].index(i)
			if len(set(neighbor_data[2][indexnum])-set(second_neighbor2)) != 0:
				for j in set(neighbor_data[2][indexnum])-set(second_neighbor2):		
					for k in nn_data[j]:
						if k[0] == i:
							diffx,diffy,diffz = firstx-k[2],firsty-k[3],firstz-k[4]
							# plot second neighbor
							ax.scatter(secondx,secondy,secondz,color='g')
							ax.text(secondx,secondy,secondz,secondtag)
							# first neighbor - second neighbor
							line = art3d.Line3D([firstx,secondx],[firsty,secondy],[firstz,secondz], color='y')
							ax.add_line(line)

		
	if len(neighbor_data[2]) == len(second_neighbor):
		for index,i in enumerate(neighbor_data[2]):
			for j in nn_data[isite][1::]:
				if j[0] == neighbor_data[1][0][index]:
					firstox,firstoy,firstoz = j[2],j[3],j[4]
			
			for j in set(i)-set(second_neighbor[index]):
				if j in nn_data:
					for k in nn_data[j]:
						if k[0] == neighbor_data[1][0][index]:
							if not j in first_neighbor:
								# plot second neighbor
								diffx,diffy,diffz = firstox-k[2],firstoy-k[3],firstoz-k[4]
								secondtag,secondx,secondy,secondz = nn_data[j][0][0]+'_'+str(j),nn_data[j][0][2]+diffx,nn_data[j][0][3]+diffy,nn_data[j][0][4]+diffz			
								ax.scatter(secondx,secondy,secondz,color='g')
								ax.text(secondx,secondy,secondz,secondtag)
								# first neighbor - second neighbor
								line = art3d.Line3D([firstox,secondx],[firstoy,secondy],[firstoz,secondz], color='y')
								ax.add_line(line)
				else:
					for k in nn_data[neighbor_data[1][0][index]]:
						if k[0] == j:
							if not k[0] in first_neighbor:
								secondtag,secondx,secondy,secondz = k[1]+'_'+str(k[0]),k[2],k[3],k[4]
								ax.scatter(secondx,secondy,secondz,color='g')
								ax.text(secondx,secondy,secondz,secondtag)
								# first neighbor - second neighbor
								line = art3d.Line3D([firstox,secondx],[firstoy,secondy],[firstoz,secondz], color='y')
								ax.add_line(line)
	
	ax.scatter(ox,oy,oz,color='b')
	ax.text(ox,oy,oz,otag)
			
	fig.savefig( cifnum + '_' + otag + ".png")
	plt.close()
		

def main():
	cwd = os.getcwd()

	parser = argparse.ArgumentParser()
	parser.add_argument('-a','--atom',required=True)
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
		#re.findall('\/(\w+)\.cif',i)[0]
		cifnum=os.path.basename(i)
		cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(i))
		with open(cifdir_nn_i_data,"rb") as frb:
			nn_data = pickle.load(frb)

		cifdir_neighbor_i_data = subprocess.getoutput("find {0} -name neighbor_data_*.pickle".format(i))
		with open(cifdir_neighbor_i_data,"rb") as frb:
			neighbor_data = pickle.load(frb)
		
		print(cifnum)
		
		#if cifnum == '1531227':
		
		for j in nn_data.keys():
			isite_atom = re.split(r'([a-zA-Z]+)',nn_data[j][0][0])[1]
			if isite_atom == args.atom:
				os.chdir(i)
				cre_plotdata(j,nn_data,neighbor_data[j],cifnum)
				os.chdir(cwd)
				#sys.exit()
				
			
if __name__ == '__main__':
	main()
	
