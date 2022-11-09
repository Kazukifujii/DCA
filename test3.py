from crystal_emd.read_info import remake_csv
dataset='cluster_dataset'
from glob import glob
clusterlist=glob('{}/*'.format(dataset))
for i in clusterlist:
    remake_csv(i,outname='remake.csv')
    break
    