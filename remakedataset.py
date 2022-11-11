from crystal_emd.read_info import remake_csv
from crystal_emd.cluster_adress_func import cluster_list


clusterlistdf=cluster_list('result/pointtest',dirs=True)

for i,data in clusterlistdf.iterrows() :
    for pattern in range(0,12):
        adress='{}/{}_{}_{}.csv'.format(data.adress,data.cifid,data.isite,pattern)
        remake_csv(adress,outname=adress)