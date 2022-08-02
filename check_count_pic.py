import os
import re
import sys
import pickle
import argparse
import subprocess

def main():
	cwd = os.getcwd()

	parser = argparse.ArgumentParser()
	parser.add_argument('-a','--atom',required=True)
	parser.add_argument('--output1', default='result')
	parser.add_argument('--output2', default='cod')
	args = parser.parse_args()

	cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(args.output1 + "/" + args.output2))
	cifdir = cifdir_.split('\n')
	del cifdir[0]

	count = 0
	for i in cifdir:
		cifnum = re.findall('\/(\d+)',i)[0]
		
		cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(i))
		with open(cifdir_nn_i_data,"rb") as frb:
			nn_data = pickle.load(frb)
				
		for j in nn_data.keys():
			isite_atom = re.split(r'([a-zA-Z]+)',nn_data[j][0][0])[1]
			
			if isite_atom == args.atom:
				count += 1
	
	print(count)
				
if __name__ == '__main__':
	main()
	
