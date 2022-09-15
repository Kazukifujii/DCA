from cmath import nan
import pandas as pd
import os,itertools,time
from distance_func import make_distance
from joblib import Parallel,delayed
import subprocess

def parallel_self_distance(clusterdf,comb,pattern_j):
    index_i,index_j=comb
    data_i=clusterdf.loc[index_i]
    data_j=clusterdf.loc[index_j]
    csvi='{}/{}_{}_0.csv'.format(data_i.adress,data_i.cifid,data_i.isite,0)
    csvj='{}/{}_{}_{}.csv'.format(data_j.adress,data_j.cifid,data_j.isite,pattern_j)
    if not (os.path.isfile(csvi) and os.path.isfile(csvj)):
        return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,nan)
    disij=make_distance(csvi,csvj)
    return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,disij)

def make_distance(listadress,resultname):
    tstime=time.perf_counter()
    if type(listadress) is str:
        all_cluser=pd.read_csv(listadress,index_col=0)
    all_index=all_cluser.index.to_list()
    comb=list(itertools.combinations(all_index,2))
    plist=[i for i in range(12)]
    alllen=12
    cont=0
    distance=list()
    for pi in plist:
        cont+=1
        print("\r"+str(cont)+'/'+str(alllen),end="")
        fstime=time.perf_counter()
        distance_=Parallel(n_jobs=-1)(delayed(parallel_self_distance)(all_cluser,comb_,pi) for comb_ in comb)
        distance+=distance_
        etiem=time.perf_counter()
        print('\ncomputation time {}'.format(etiem-fstime))
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    distancedf.to_csv('{}/{}'.format(dir,resultname))
    print()
    print('output {}'.format(resultname))
    print('total computation time {}'.format(etiem-tstime))

