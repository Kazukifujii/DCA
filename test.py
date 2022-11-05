from crystal_emd.read_cryspy_info import isolation_poscars
from crystal_emd.read_cryspy_info import read_sitinfo_poscar
from crystal_emd.read_cryspy_info import make_nnlist
from crystal_emd.read_cryspy_info import make_nn_data_from_nnlist

isolation_poscars('result/testdir/init_POSCARS')
siteinfo=read_sitinfo_poscar('result/testdir/ID_0_POSCAR')
make_nnlist('result/testdir/ID_0_POSCAR',rmax=10.0)
make_nn_data_from_nnlist('result/testdir/ID_0_POSCAR.nnlist',siteinfo=siteinfo)
