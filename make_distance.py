from crystal_emd.cluster_adress_func import isite_list,fcluster_list
from crystal_emd.distance_func import make_distance_csv
import pandas as pd
from crystal_emd.clustering_func import make_clusering
import os
from crystal_emd.read_info import make_sort_ciffile
from crystal_emd.distance_func import remake_distance
dir='result/testcif'

make_sort_ciffile(dir)
cifdir=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
cwd = os.getcwd()
errorid=list()

for i in cifdir:
    cifid=os.path.basename(i)
    print(cifid)
    listadress_=isite_list(i)
    make_distance_csv(listadress=listadress_,resultname="{}/{}_self_distance".format(i,cifid))
    remake_distance("{}/{}_self_distance".format(i,cifid))
    flusterdf=make_clusering(csvadress="{}/{}_self_distance_remake".format(i,cifid),csvn="{}/{}_sort_distance".format(i,cifid),pngn='{}/{}_self_distance.png'.format(i,cifid))
    flusterdf.to_csv("{}/{}_fcluster".format(i,cifid))
fclusterdf=fcluster_list(dir)

make_distance_csv(listadress=fclusterdf,resultname ='{}/all_distance'.format(dir))

remake_distance('{}/all_distance'.format(dir))

make_clusering(csvadress='{}/all_distance_remake'.format(dir),csvn="{}/all_sort_distance".format(dir),pngn="{}/all_cluster.png".format(dir))
