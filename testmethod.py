import glob,time
import pandas as pd
import os,subprocess,itertools,re
from distance_func import make_distance
from joblib import Parallel,delayed
def parallel_self_distance(dir,cifid,comb,pattern_j):
    isite_i,isite_j=comb
    csvi='{}/{}_{}_0.csv'.format(dir,cifid,isite_i,0)
    csvj='{}/{}_{}_{}.csv'.format(dir,cifid,isite_j,pattern_j)
    disij=make_distance(csvi,csvj)
    return (isite_i,isite_j,0,pattern_j,disij)

tstime=time.perf_counter()
cifdirs_ = subprocess.getoutput("find {0} -type d | sort".format('result/sorttest'))
cifdirs = cifdirs_.split('\n')
del cifdirs[0]
for  i,cifdir in  enumerate(cifdirs):
    stime=time.perf_counter()
    cifid=re.split('/',cifdir)[-1]
    print(cifid)
    csvname='{}_self_distance.csv'.format(cifid)
    ciflist=glob.glob('{}/{}_[0-9]*.csv'.format(cifdir,cifid))
    isitelist=[re.findall('[0-9]{1,}',csvname)[0] for csvname in ciflist]
    plist=[re.findall('[0-9]{1,}',csvname)[1] for csvname in ciflist]
    isitelist=list(set(isitelist))
    plist=list(set(plist))
    isitelist=[int(isitelist_) for isitelist_ in isitelist]
    plist=[int(plist_) for plist_ in plist]
    isitelist.sort()
    plist.sort()
    comb=list(itertools.combinations(isitelist,2))
    distance=list()
    alllen=len(plist)
    cont=0
    for pi in plist:
        cont+=1
        print("\r"+str(cont)+'/'+str(alllen),end="")
        distance_=Parallel(n_jobs=16)(delayed(parallel_self_distance)(cifdir,cifid,comb_,pi) for comb_ in comb)
        distance+=distance_
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    distancedf.to_csv('{}/{}'.format(cifdir,'paralleltest.csv'))
    print()
    print('output {}'.format(csvname))
    etiem=time.perf_counter()
    print('computation time {}'.format(etiem-stime))
    break

print('total computation time {}'.format(etiem-tstime))