import os,pickle,subprocess,re
from crystal_emd.read_info import Set_Cluster_Info

cifdir=['read_cryspy/init_poscars']
cwd = os.getcwd()
for i in cifdir:
    cifid=os.path.basename(i)
    print(cifid)
    cifdir_nn_i_data = subprocess.getoutput("find {0}/*.pickle".format(i))
    with open(cifdir_nn_i_data,"rb") as frb:
        nn_data = pickle.load(frb)
    alllen_=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            alllen_+=1
    cont=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            cluster=Set_Cluster_Info(isite,nn_data,2)
            from crystal_emd.read_info import clusterplot as clp
            clp(clusterdf=cluster.cluster_coords,show=True)
    os.chdir(cwd)
    #print()
