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
        for j in list(neighbor_data.keys()):
            print(j,':',neighbor_data[j])
        sys.exit()
        for j in nn_data.keys():
            isite_atom = re.split(r'([a-zA-Z]+)',nn_data[j][0][0])[1]
            if isite_atom == args.atom:
                os.chdir(i)
                cre_plotdata(j,nn_data,neighbor_data[j],cifnum)
                os.chdir(cwd)
				#sys.exit()
				
			
if __name__ == '__main__':
	main()
	
