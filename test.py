from crystal_emd.cluster_pointing import make_crystall_point
from crystal_emd.cluster_adress_func import cluster_list
import os,sys
d=make_crystall_point('cluster_dataset')
resulttxt='result/randzeo/pointlist'
text_file=open(resulttxt,'w')
text_file.write('cifid,point\n')
text_file.close()
from glob import glob
clusteradress_list=glob('result/randzeo/*')

for i,cifadress in enumerate(clusteradress_list):
    print(cifadress)
    ddd=cluster_list(cifadress)
    cifid=os.path.basename(cifadress)
    print('{}/{}'.format(i+1,len(clusteradress_list)))
    print(cifid)
    d.cal_crystal_point(cifadress,n_job=-1)
    text_file=open(resulttxt,'a')
    text_file.write('{},{}\n'.format(cifid,d.crystal_point))
    text_file.close()
    break