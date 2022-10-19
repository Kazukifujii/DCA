from crystal_emd.cluster_adress_func import isite_list,fcluster_list
from crystal_emd.distance_func import make_distance_csv
import pandas as pd
from crystal_emd.clustering_func import make_clusering
import os
dir='result/testcif'
cifdir=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
cwd = os.getcwd()
errorid=list()

for i in cifdir:
    cifid=os.path.basename(i)
    print(cifid)
    listadress_=isite_list(i)
    make_distance_csv(listadress=listadress_,resultname="{}/{}_self_distance.csv".format(i,cifid))
    flusterdf=make_clusering(csvadress="{}/{}_self_distance.csv".format(i,cifid),csvn="{}/{}_sort_distance.csv".format(i,cifid),pngn='{}/{}_self_distance.png'.format(i,cifid))
    flusterdf.to_csv("{}/{}_fcluster.csv".format(i,cifid))

fclusterdf=fcluster_list(dir)

make_distance_csv(listadress=fclusterdf,resultname ="all_distance.csv")
alldistance=pd.read_csv("all_distance.csv",index_col=0)
make_clusering(csvadress="matrix_all_sort_distance.csv",csvn="all_sort_distance.csv",pngn="all_cluster.png",cal_matrixdf=False)