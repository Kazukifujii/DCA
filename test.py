from crystal_emd.read_cryspy_info import isolation_poscars
from crystal_emd.read_cryspy_info import read_sitinfo_poscar
from crystal_emd.read_cryspy_info import make_nnlist
from crystal_emd.read_cryspy_info import make_nn_data_from_nnlist
"""
isolation_poscars('result/testdir/init_POSCARS')
siteinfo=read_sitinfo_poscar('result/testdir/ID_0_POSCAR')
make_nnlist('result/testdir/ID_0_POSCAR',rmax=10.0)
make_nn_data_from_nnlist('result/testdir/ID_0_POSCAR.nnlist',siteinfo=siteinfo)
"""

from crystal_emd.read_info import Set_Cluster_Info

dir='result/testposcar/ID_0/ID_0_POSCAR.pickle'
import pickle
with open(dir,'rb') as f:
    nn_data=pickle.load(f)
f=Set_Cluster_Info(isite=1,nn_data_=nn_data,adjacent_number=2)
f.parallel_shift_of_center()
f.rotation(pattern=1)
from crystal_emd.read_info import clusterplot
print(f.cluster_coords)
clusterplot(f.cluster_coords,show=True)