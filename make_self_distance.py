from distance_func import make_distance
import glob,time
import pandas as pd
import os,subprocess,itertools,re

stime=time.perf_counter()
cifdirs_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod'))
cifdirs = cifdirs_.split('\n')
del cifdirs[0]

cwd = os.getcwd()
for cifdir in cifdirs:
    dirname=re.split('/',cifdir)[-1]
    print(dirname)
    csvname='{}_self_distance.csv'.format(dirname)
    csvlist=glob.glob(cifdir+'/*csv')
    distance=list()
    cifcomb=list(itertools.combinations(csvlist,2))
    comblen=str(len(cifcomb))
    cont=0
    for i,j in cifcomb:
        print("\r"+str(cont)+'/'+comblen,end="")
        isite_i,pattern_i=tuple(re.findall('(?=_)*\d{1,}',i))
        isite_j,pattern_j=tuple(re.findall('(?=_)*\d{1,}',j))
        distance_=make_distance(i,j)
        distance.append((isite_i,isite_j,pattern_i,pattern_j,distance_))
        cont+=1
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    distancedf.to_csv('{}/{}'.format(cifdir,csvname))
    print('output {}'.format(csvname))
    etiem=time.perf_counter()
    print('end time {}'.format(stime-etiem))