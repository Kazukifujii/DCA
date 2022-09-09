from cmath import nan
import glob,time
import pandas as pd
import os,subprocess,itertools,re
from distance_func import make_distance
from joblib import Parallel,delayed
def parallel_self_distance(clusterdf,comb,pattern_j):
    index_i,index_j=comb
    data_i=clusterdf.loc[index_i]
    data_j=clusterdf.loc[index_j]
    csvi='{}/{}_{}_0.csv'.format(data_i.adress,data_i.cifid,data_i.isite,0)
    csvj='{}/{}_{}_{}.csv'.format(data_j.adress,data_j.cifid,data_j.isite,0)
    if not (os.path.isfile(csvi) and os.path.isfile(csvj)):
        return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,nan)
    disij=make_distance(csvi,csvj)
    return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,disij)

tstime=time.perf_counter()

dir='result/allzeorite'
outcsvname='all_distance.csv'
all_cluser=pd.read_csv('{}/allcif_cluster'.format(dir),index_col=0)
all_index=all_cluser.index.to_list()
comb=list(itertools.combinations(all_index,2))

stime=time.perf_counter()
plist=[i for i in range(12)]
alllen=12
cont=0
distance=list()
for pi in plist:
    cont+=1
    print("\r"+str(cont)+'/'+str(alllen),end="")
    distance_=Parallel(n_jobs=12)(delayed(parallel_self_distance)(all_cluser,comb_,pi) for comb_ in comb)
    distance+=distance_
disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
distancedf=pd.DataFrame(distance,columns=disfile_colname)
distancedf.to_csv('{}/{}'.format(dir,outcsvname))
print()
print('output {}'.format(outcsvname))
etiem=time.perf_counter()
print('computation time {}'.format(etiem-stime))
print('total computation time {}'.format(etiem-tstime))
