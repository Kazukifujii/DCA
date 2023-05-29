from Distance_based_on_Cluster_Analysis.make_nnlist_info import make_poscar
from subprocess import run
from glob import glob
#a.outは単位格子内の各原子に対して、指定した半径(rmax)内に存在する原子をリストアップするプログラムになっている
filepath='datas/cifdirs/testcif/ABW.cif'#cifのパス
rmax=10#半径    
#make_poscar(filepath)

poscarpath=glob('*.poscar')

#ターミナルを開いて次のコマンドを打つ
#a.out ABW.cif.poscar 10