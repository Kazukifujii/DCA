#poscarからnn_dataを各ディレクトリごとに作成する
import os,subprocess,glob,re,sys
indir='indirs/testposcar'
resultdir='result/{}'.format(os.path.basename(indir))
poscarfils=glob.glob('{}/*POSCAR'.format(indir))

import shutil
if os.path.exists(resultdir):
    shutil.rmtree(resultdir)
os.mkdir(resultdir)
from crystal_emd.read_cryspy_info import make_nnlist,make_nn_data_from_nnlist,read_sitinfo_poscar
cwd=os.getcwd()
for path in poscarfils:
    name=re.sub('.POSCAR','',os.path.basename(path))
    poscarname=os.path.basename(path)
    resultdir_i='{}/{}'.format(resultdir,name)
    os.mkdir(resultdir_i)
    shutil.copy(path,resultdir_i)
    os.chdir(resultdir_i)
    make_nnlist(fileadress=poscarname,rmax=10.0)
    siteinfo=read_sitinfo_poscar(poscarname)
    nnlistname=glob.glob('*nnlist')
    make_nn_data_from_nnlist(nnlistname[0],siteinfo=siteinfo)
    os.chdir(cwd)

from crystal_emd.read_info import Set_Cluster_Info
import pickle
nn_data_dirs=glob.glob('{}/*'.format(resultdir))
for i in nn_data_dirs:
    cifid=os.path.basename(i)
    print(cifid)
    cifdir_nn_i_data = subprocess.getoutput("find {}/*pickle".format(i))
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
            cluster=Set_Cluster_Info(isite,nn_data,2)
            alllen=alllen_*len(cluster.shaft_comb)
            cluster.parallel_shift_of_center()
            for pattern in range(len(cluster.shaft_comb)):
                cont+=1
                print("\r{}/{}".format(cont,alllen),end="")
                #print("\r{}/{}".format(isite,pattern),end="")
                #print("\risite={},pattrn={}".format(isite,pattern),end="")
                cluster.rotation(pattern=pattern)
                cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
                #clp(clusterdf=cluster.cluster_coords,title='{}_{}_{}.png'.format(cifid,isite,pattern))
    os.chdir(cwd)
    print()