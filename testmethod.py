import os,pickle
import subprocess
from read_info import Set_Cluster_Info
from read_info import clusterplot as clp
import re

def make_cluster_csv(datdir,fatom='Si',outdir=False,rotat=True,show=None):
    cwd = os.getcwd()
    if outdir==False:
        outdir=datdir
    cifid=os.path.basename(datdir)
    cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(datdir))
    with open(cifdir_nn_i_data,"rb") as frb:
        nn_data = pickle.load(frb)
    cifdir_neighbor_i_data = subprocess.getoutput("find {0} -name neighbor_data_*.pickle".format(datdir))
    with open(cifdir_neighbor_i_data,"rb") as frb:
        neighbor_data = pickle.load(frb)
    os.chdir(outdir)
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == fatom:
            cluster=Set_Cluster_Info(isite,nn_data,4)
            if rotat:
                for pattern in range(len(cluster.shaft_comb)):
                    print(outdir)
                    cluster.parallel_shift_of_center()
                    cluster.rotation(pattern=pattern)
                    cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
            else:
                cluster.parallel_shift_of_center()
                cluster.cluster_coords.to_csv('{}_{}.csv'.format(cifid,isite))
                clp(cluster.cluster_coords,title='{}_{}.png'.format(cifid,isite),show=show)
    os.chdir(cwd)


import subprocess
outdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod/*image'))
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod'))
cifdir = cifdir_.split('\n')
del cifdir[0]
outdir = outdir_.split('\n')


outdir.sort()
cifdir=list(set(cifdir)-set(outdir))
cifdir.sort()

for i,cifadress in enumerate(cifdir):
    make_cluster_csv(cifadress,outdir=outdir[i],rotat=False)
