#データセットのマッチング


import pandas as pd
import time
from joblib import Parallel,delayed
from crystal_emd.distance_func import parallel_self_distance
from crystal_emd.cluster_adress_func import cluster_list
import os,re
datasetadress='cluster_dataset'
cluster_adress='result/pointtest/ABW/ABW_0_0.csv'
from crystal_emd.cluster_pointing import make_cluster_point
d=make_cluster_point(datasetadress=datasetadress)
p=d.point(cluster_adress,n_job=-1)
print(p)