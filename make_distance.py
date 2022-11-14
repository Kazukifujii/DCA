from crystal_emd.cluster_adress_func import isite_list,fcluster_list
from crystal_emd.distance_func import make_distance_csv
import pandas as pd
from crystal_emd.clustering_func import make_clusering
import os
from crystal_emd.read_info import make_sort_ciffile
from crystal_emd.distance_func import remake_distance
dir='cluster_dataset'

make_sort_ciffile(dir,estimecont='all')
cifdir=pd.read_csv('{}/picupadress'.format(dir),index_col=0)
cwd = os.getcwd()
errorid=list()
cont=0
for i,data in cifdir.iterrows():
    cifid=data.cifid
    print(cifid)
    listadress_=isite_list(data.cifadress)
    make_distance_csv(listadress=listadress_,resultname="{}/{}_self_distance".format(data.cifadress,cifid))
    remake_distance("{}/{}_self_distance".format(data.cifadress,cifid))
    flusterdf=make_clusering(csvadress="{}/{}_self_distance_remake".format(data.cifadress,cifid),csvn="{}/{}_sort_distance".format(data.cifadress,cifid),pngn='{}/{}_self_distance.png'.format(data.cifadress,cifid))
    flusterdf.to_csv("{}/{}_fcluster".format(data.cifadress,cifid))

fclusterdf=fcluster_list(dir)
print(fclusterdf)
make_distance_csv(listadress=fclusterdf,resultname ='{}/all_distance'.format(dir))

remake_distance('{}/all_distance'.format(dir))

all_fcluster=make_clusering(csvadress='{}/all_distance_remake'.format(dir),csvn="{}/all_sort_distance".format(dir),pngn="{}/all_cluster.png".format(dir))
all_fcluster.to_csv('{}/all_fcluster'.format(dir))