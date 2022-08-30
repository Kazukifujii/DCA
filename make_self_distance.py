
import glob,time
import pandas as pd
import os,subprocess,itertools,re
from distance_func import make_distance
stime=time.perf_counter()
cifdirs_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod'))
cifdirs = cifdirs_.split('\n')
del cifdirs[0]

cwd = os.getcwd()
for  cifdir in  cifdirs:
    os.chdir(cifdir)
    dirname=re.split('/',cifdir)[-1]
    print(dirname)
    csvname='{}_self_distance.csv'.format(dirname)
    ciflist=glob.glob('*[0-9]*_[0-9].csv')
    isitelist=[re.findall('[0-9]{1,}',csvname)[0] for csvname in ciflist]
    plist=[re.findall('[0-9]{1,}',csvname)[1] for csvname in ciflist]
    isitelist=list(set(isitelist))
    plist=list(set(plist))
    isitelist.sort()
    plist.sort()
    comb=list(itertools.combinations(isitelist,2))
    distance=list()
    alllen=len(comb)*len(plist)
    cont=0
    for comb in itertools.combinations(isitelist,2):
        isite_i,isite_j=comb
        csvi=glob.glob('*{}_0.csv'.format(isite_i,0))[0]
        for pi in plist:
            try:
                cont+=1
                print("\r"+str(cont)+'/'+str(alllen),end="")
                csvj=glob.glob('*{}_{}.csv'.format(isite_j,pi))[0]
                disij=make_distance(csvi,csvj)
                distance.append((isite_i,isite_j,plist[0],pi,disij))
            except:
                print(isite_i,isite_j,plist[0],pi)
                continue
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    distancedf.to_csv(csvname)
    print()
    print('output {}'.format(csvname))
    etiem=time.perf_counter()
    print('end time {}'.format(etiem-stime))
    os.chdir(cwd)