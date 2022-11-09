#データセットのマッチング


import pandas as pd
import time
from joblib import Parallel,delayed
from crystal_emd.distance_func import parallel_self_distance
from crystal_emd.cluster_adress_func import cluster_list
import os,re
def make_cluster_point(clusteradress,datasetadress,outdir=False):
    #listadressの設定
    tstime=time.perf_counter()
    datalist=cluster_list(datasetadress)
    dirname=os.path.dirname(clusteradress)
    basename=os.path.basename(clusteradress)
    isite=int(re.split('_',basename)[-2])
    cifid=re.sub('_[0-9]*_[0-9]*\.csv','',basename)
    datalist_=pd.DataFrame([cifid,dirname,isite],index=datalist.columns.to_list())
    datalist=pd.concat([datalist,datalist_.T],ignore_index=True)
    comb=[(datalist.index.to_list()[-1],i) for i in datalist.index.to_list()[0:-1]]
    plist=[i for i in range(12)]
    alllen=12
    cont=0
    distance=list()
    for pi in plist:
        cont+=1
        print("\r"+str(cont)+'/'+str(alllen),end="")
        fstime=time.perf_counter()
        distance_=Parallel(n_jobs=6)(delayed(parallel_self_distance)(datalist,comb_,pi) for comb_ in comb)
        distance+=distance_
        etiem=time.perf_counter()
        print('\ncomputation time {}'.format(etiem-fstime))
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    distancedf.to_csv('{}/{}_{}_distance.csv'.format(dirname,basename,os.path.basename(datasetadress)))
    print('total computation time {}'.format(etiem-tstime))
    return distancedf.sort_values(by='distance').iloc[0].distance

datasetadress='cluster_dataset'
cluster_adress='result/testposcar/ID_0/ID_0_1_0.csv'
point=make_cluster_point(clusteradress=cluster_adress,datasetadress=datasetadress)
print(point)