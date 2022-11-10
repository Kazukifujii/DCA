from crystal_emd.cluster_pointing import make_crystall_point
from crystal_emd.cluster_adress_func import cluster_list

d=make_crystall_point('cluster_dataset')
import pandas as pd
resulttxt='result/allzeorite/cifpoint'
text_file=open(resulttxt,'w')
text_file.write('cifid,point')
text_file.close()
import sys
text_file=open(resulttxt,'w')
cifid,cluster_point="ABW",10
text_file.write('{},{}\n'.format(cifid,cluster_point))
text_file.close()
sys.exit()
cifadress_list=pd.read_csv('result/allzeorite/picupadress',index_col=0).cifadress.to_list()
import os
for cifadress in cifadress_list:
  cifid=os.path.basename
  print(cifid)
  d.cad_crystal_point(cifadress)
  text_file=open(resulttxt,'w')
  text_file.write(cifid,d.cluster_point)
  text_file.close()