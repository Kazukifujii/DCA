import re
import sys
from make_cluster_adress import make_classification_ring,make_fcluster_list
from make_distance import make_distance_csv
import pandas as pd

dir='result/allzeorite'
import os

#mfl=make_fcluster_list(dir)
#make_classification_ring(mfl,outdir=dir)

from glob import glob as gl

"""mcr=gl('{}/*ring*'.format(dir))
for ringadress in mcr:
    ringnum=re.split('=',ringadress)[1]
    make_distance_csv(ringadress,resultname='all_distance_ring={}'.format(ringnum),outdir=dir)"""

from make_clustering import make_clusering

distancecsv=gl('{}/all_distance*=*'.format(dir))
for csvadress in distancecsv:
    print(csvadress)
    ringnum=re.split('=',csvadress)[1]
    print(ringnum)
    make_clusering(csvadress,csvn='{}/sort_distance_clustering_ring={}.csv'.format(dir,ringnum),pngn='{}/cluster_ring={}.png'.format(dir,ringnum))

