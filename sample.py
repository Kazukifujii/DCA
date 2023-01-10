from Distance_based_on_Cluster_Analysis import make_nnlist_info as mni
#cifファイルのアドレス
import os,shutil
cifadress='cifdirs/testcif/ABW.cif'
cifname=os.path.basename(cifadress)

#サンプルディレクトリの作成
resultdir='result/sample'
if os.path.isdir(resultdir):
    #同じ名前のディレクトリを削除
    shutil.rmtree(resultdir)
os.mkdir(resultdir)

#cifファイルのコピー
shutil.copyfile(cifadress,'{}/{}'.format(resultdir,cifname))
cwd=os.getcwd()

#感とディレクトリの移動
os.chdir(resultdir)

mni.make_poscar(cifname)
mni.make_nnlist('{}.poscar'.format(cifname),rmax=3.5)
siteinfo=mni.read_sitinfo_poscar('{}.poscar'.format(cifname))
mni.make_nn_data_from_nnlist('{}.poscar.nnlist'.format(cifname),siteinfo)