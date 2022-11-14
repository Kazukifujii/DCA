#reduce dataset
from crystal_emd.cluster_adress_func import fcluster_list
resultdir='database'
orignal_dataset='cluster_dataset'
fclusterdf=fcluster_list(orignal_dataset)
import shutil,os

if os.path.isdir(resultdir):
    shutil.rmtree(resultdir)

os.mkdir(resultdir)
for i,data in fclusterdf.iterrows():
    for pattern in range(12):
        clusteradress='{}/{}_{}_{}.csv'.format(data.adress,data.cifid,data.isite,pattern)
        if not os.path.isfile(clusteradress):
            print('not file ',clusteradress)
        copyadress='{}/{}_{}_{}.csv'.format(resultdir,data.cifid,data.isite,pattern)
        shutil.copy(clusteradress,copyadress)