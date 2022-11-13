from subprocess import run,getoutput
from crystal_emd.read_info import make_sort_ciffile
import shutil,os,re,pickle
import pandas as pd
from crystal_emd.read_info import Set_Cluster_Info
from crystal_emd.cluster_adress_func import cluster_list

basedataset='result/allzeorite'
datasetdir='cluster_dataset'
"""
ciflist=make_sort_ciffile(basedataset,estimecont='all')
if os.path.isdir(datasetdir):
        shutil.rmtree(datasetdir)

#for sampleadress in d.sample(100,random_state=0).cifadress.to_list():
for i,sampleadress in enumerate(ciflist.iloc[0:100].cifadress.to_list()):
    print('\r{}/100'.format(i+1),end='')
    copyadress='cluster_dataset/{}'.format(os.path.basename(sampleadress))
    if os.path.isdir(copyadress):
        shutil.rmtree(copyadress)
    shutil.copytree(sampleadress,copyadress)
"""
#cheak all csvfile
cwd=os.getcwd()
ciflist=make_sort_ciffile(datasetdir,estimecont='all')
CONT=0
for i,data in ciflist.iterrows():
    cifid=os.path.basename(data.cifadress)
    clusterlist=cluster_list(data.cifadress)
    if clusterlist.shape[0]==0:
        print(cifid)
        os.chdir(data.cifadress)
        cifdir_nn_i_data = getoutput("find nb_*.pickle")
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
                alllen=alllen_
                cont+=1
                print("\r"+str(cont)+'/'+str(alllen),end="")
                cluster.parallel_shift_of_center()
                cluster.rotation()
                cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,0))
        os.chdir(cwd)
    clusterlist=cluster_list(data.cifadress)
    os.chdir(data.cifadress)
    for i2,data2 in clusterlist.iterrows():
        csvadress='{}_{}_0.csv'.format(data2.cifid,data2.isite)
        df=pd.read_csv(csvadress,index_col=0)
        cluster=Set_Cluster_Info(clusterdf=df)
        #alllen=alllen_*len(cluster.shaft_comb)
        isite=df.iloc[0].isite
        for pattern in range(len(cluster.shaft_comb)):
            #print("\r"+str(cont)+'/'+str(alllen),end="")
            cluster.parallel_shift_of_center()
            cluster.rotation(pattern=pattern)
            cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
    os.chdir(cwd)
    print()

