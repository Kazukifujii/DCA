import os,pickle,subprocess,re
from crystal_emd.read_info import Set_Cluster_Info
import pandas as pd


dir='result/allzeorite'
cifdir=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
cwd = os.getcwd()
for i in cifdir:
    cifid=os.path.basename(i)
    print(cifid)
    cifdir_nn_i_data = subprocess.getoutput("find {0} -name nb_*.pickle".format(i))
    with open(cifdir_nn_i_data,"rb") as frb:
        nn_data = pickle.load(frb)
    alllen_=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            alllen_+=1
    cont=0
    os.chdir(i)
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            cluster=Set_Cluster_Info(isite,nn_data,2)#隣接数
            alllen=alllen_*len(cluster.shaft_comb)
            for pattern in range(len(cluster.shaft_comb)):
                cont+=1
                print("\r"+str(cont)+'/'+str(alllen),end="")
                cluster.parallel_shift_of_center()
                cluster.rotation(pattern=pattern)
                cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
    os.chdir(cwd)
    print()
