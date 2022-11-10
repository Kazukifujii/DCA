from glob import glob as gl
import random,sys
from crystal_emd.cluster_pointing import make_cluster_point
datasetadress='result/allzeorite'
import pandas as pd
d=pd.read_csv('result/allzeorite/picupadress',index_col=0)

import shutil,os
for sampleadress in d.sample(100,random_state=0).cifadress.to_list():
    copyadress='cluster_dataset/{}'.format(os.path.basename(sampleadress))
    if os.path.isdir(copyadress):
        shutil.rmtree(copyadress)
    shutil.copytree(sampleadress,copyadress)