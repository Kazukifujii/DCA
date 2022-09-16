from make_distance import make_distance_csv
from make_cluster_adress import fcluster_list,isite_list,classification_ring_list
import pandas as pd
import os

dir='result/allzeorite'
cifdirs=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
cwd = os.getcwd()
for cifdir in cifdirs:
    break