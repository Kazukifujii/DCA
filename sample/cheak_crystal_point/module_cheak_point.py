from crystal_emd.cluster_pointing import make_crystall_point
from crystal_emd.cluster_adress_func import cluster_list

d=make_crystall_point('cluster_dataset')
import pandas as pd
resulttxt='result/allzeorite/cifpoint'
text_file=open(resulttxt,'w')
text_file.write('cifid,point\n')
text_file.close()
cifadress_list=pd.read_csv('result/allzeorite/picupadress',index_col=0).cifadress.to_list()
import os
for i,cifadress in enumerate(cifadress_list):
  cifid=os.path.basename(cifadress)
  print('cif {}/{}'.format(i+1,len(cifadress_list)))
  print(cifid)
  d.cal_crystal_point(cifadress,n_job=-1)
  text_file=open(resulttxt,'a')
  text_file.write('{},{}\n'.format(cifid,d.crystal_point))
  text_file.close()
  if i==3:
    break