from glob import glob as gl
import random,sys
import shutil,os
datasetadress='result/allzeorite'
import pandas as pd
from crystal_emd.read_info import make_sort_ciffile
make_sort_ciffile(datasetadress,estimecont='all')
d=pd.read_csv('result/allzeorite/picupadress',index_col=0)
datasetdir='cluster_dataset'
if os.path.isdir(datasetdir):
        shutil.rmtree(datasetdir)

#for sampleadress in d.sample(100,random_state=0).cifadress.to_list():
for i,sampleadress in enumerate(d.iloc[0:100].cifadress.to_list()):
    print('\r{}/100'.format(i+1),end='')
    copyadress='cluster_dataset/{}'.format(os.path.basename(sampleadress))
    if os.path.isdir(copyadress):
        shutil.rmtree(copyadress)
    shutil.copytree(sampleadress,copyadress)