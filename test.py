from crystal_emd.distance_func import make_distance_csv,recal_distance
from crystal_emd.cluster_adress_func import cluster_list
clusterlistdf=cluster_list('result/pointtest/ABW')
make_distance_csv(clusterlistdf,resultname='testdistance_abw.csv')
from crystal_emd.clustering_func import make_clusering
import pandas as pd
import os

recal_distance('testdistance_abw.csv')
fluster=make_clusering('testdistance_abw_remake.csv',pngn='test.svg')
print(fluster)