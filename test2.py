from crystal_emd.cluster_pointing import make_crystall_point
from crystal_emd.cluster_adress_func import cluster_list
d=cluster_list('result/pointtest/ABW')


d=make_crystall_point('cluster_dataset')
d.cal_crystal_point('result/pointtest/ABW')
print(d.crystal_point)