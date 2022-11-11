from crystal_emd.read_info import remake_csv
from crystal_emd.cluster_adress_func import cluster_list
import sys,os
clusterlistdf=cluster_list('result/allzeorite',dirs=True)
alllen=clusterlistdf.shape[0]*12
cont=0



for i,data in clusterlistdf.iterrows() :
    for pattern in range(0,12):
        cont+=1
        print('\r{}/{}'.format(cont,alllen),end="")
        adress='{}/{}_{}_{}.csv'.format(data.adress,data.cifid,data.isite,pattern)
        if not os.path.isfile(adress):
            continue
        #print(adress)
        remake_csv(adress,outname=adress)