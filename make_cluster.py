import os,pickle
import subprocess
from read_info import Set_Cluster_Info



from read_info import clusterplot as clp
import re
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod'))
cifdir = cifdir_.split('\n')
del cifdir[0]

cwd = os.getcwd()
for i in cifdir:
    cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(i))
    with open(cifdir_nn_i_data,"rb") as frb:
        nn_data = pickle.load(frb)

    cifdir_neighbor_i_data = subprocess.getoutput("find {0} -name neighbor_data_*.pickle".format(i))
    with open(cifdir_neighbor_i_data,"rb") as frb:
        neighbor_data = pickle.load(frb)

    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            os.chdir(i)
            cluster=Set_Cluster_Info(isite,nn_data,4)
            cluster.parallel_shift_of_center()
            cluster.rotation()
            cluster.cluster_coords.to_csv('cluster_%d.csv'%isite)
            clp(cluster.cluster_coords,title='cluster%d.png'%isite)
            os.chdir(cwd)
