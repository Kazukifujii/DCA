from glob import glob as gl
import random,sys
import shutil,os
datasetadress='result/allzeorite'
import pandas as pd
d=pd.read_csv('result/allzeorite/picupadress',index_col=0)
datasetdir='cluster_dataset'
if os.path.isdir(datasetdir):
        shutil.rmtree(datasetdir)

for sampleadress in d.sample(100,random_state=0).cifadress.to_list():
    copyadress='cluster_dataset/{}'.format(os.path.basename(sampleadress))
    if os.path.isdir(copyadress):
        shutil.rmtree(copyadress)
    shutil.copytree(sampleadress,copyadress)