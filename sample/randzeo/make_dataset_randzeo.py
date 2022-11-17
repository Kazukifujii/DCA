#poscarからnn_dataを各ディレクトリごとに作成する
import os,subprocess,re,pickle,sys
from crystal_emd.read_info import Set_Cluster_Info
from crystal_emd.read_randzeo import make_nn_data_from_randzeo,make_randzeo
from glob import glob
import shutil

resultdir='result/randzeo'
filenum=1000
adjacent_num=1
cwd=os.getcwd()

#randzeoファイルを作成
make_randzeo(file_num=filenum,outdir=resultdir)
filelist=glob('{}/*randzeo'.format(resultdir))

for i,path in enumerate(filelist):
    filename=os.path.basename(path)
    fileid=filename.replace('.randzeo','')
    dirname=os.path.dirname(path)
    os.mkdir('{}/{}'.format(dirname,fileid))
    shutil.move(path,'{}/{}/'.format(dirname,fileid))

dirlist=glob('{}/*'.format(resultdir))
from crystal_emd.make_cluster import make_cluster_dataset
from glob import glob
for diradress in dirlist:
    cifid=os.path.basename(diradress)
    filename=glob('{}/*.randzeo'.format(diradress))[0]
    nn_data=make_nn_data_from_randzeo(filename=filename)
    make_cluster_dataset(cifid=cifid,nn_data=nn_data,adjacent_num=1,outdir=diradress,rotation=False)