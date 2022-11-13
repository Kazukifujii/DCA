#poscarからnn_dataを各ディレクトリごとに作成する
import os,subprocess,re,pickle,sys
from crystal_emd.read_info import Set_Cluster_Info
from crystal_emd.read_randzeo import make_nn_data_from_randzeo,make_randzeo
from glob import glob

resultdir='result/randzeo'
filenum=3
adjacent_num=2
cwd=os.getcwd()
"""
#randzeoファイルを作成
make_randzeo(file_num=filenum,outdir=resultdir)
filelist=glob('{}/*randzeo'.format(resultdir))



import shutil
for i,path in enumerate(filelist):
    filename=os.path.basename(path)
    fileid=filename.replace('.randzeo','')
    dirname=os.path.dirname(path)
    os.mkdir('{}/{}'.format(dirname,fileid))
    shutil.move(path,'{}/{}/'.format(dirname,fileid))
"""
dirlist=glob('{}/*'.format(resultdir))

for i in dirlist:
    cifid=os.path.basename(i)
    print(cifid)
    os.chdir(i)
    filename=glob('*.randzeo')[0]
    nn_data=make_nn_data_from_randzeo(filename=filename)
    alllen_=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            alllen_+=1
    cont=0
    for isite in nn_data.keys():
        isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
        if isite_atom == 'Si':
            cluster=Set_Cluster_Info(isite,nn_data,adjacent_number=adjacent_num)
            alllen=alllen_*len(cluster.shaft_comb)
            cluster.parallel_shift_of_center()
            for pattern in range(len(cluster.shaft_comb)):
                cont+=1
                print("\r{}/{}".format(cont,alllen),end="")
                cluster.rotation(pattern=pattern)
                cluster.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
    os.chdir(cwd)
    print()
