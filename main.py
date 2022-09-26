import re
dir='result/allzeorite'
import os

from glob import glob as gl
from clustering_func import make_clusering

distancecsv=gl('{}/all_distance*=*'.format(dir))
for csvadress in distancecsv:
    print(csvadress)
    ringnum=re.split('=',csvadress)[1]
    print(ringnum)
    make_clusering(csvadress,csvn='{}/sort_distance_clustering_ring={}.csv'.format(dir,ringnum),pngn='{}/cluster_ring={}.png'.format(dir,ringnum))

