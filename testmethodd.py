from distance_func import make_distance
import glob
import re
resultdir='result/cod'
dir1='result/cod/ABW'
dir2='result/cod/ACO'
csvname='distance_{}_{}.csv'.format(re.split('/',dir1)[-1],re.split('/',dir2)[-1])


csvlist2=glob.glob(dir1+'/*csv')
distance=dict()
cont=0
for i in csvlist2:
    for j in csvlist2:
        if cont==2:
            break
        isite_i,pattern_i=tuple(re.findall('(?=_)*\d{1,}',i))
        isite_j,pattern_j=tuple(re.findall('(?=_)*\d{1,}',j))
        distance_=make_distance(i,j)
        if distance.keys not in(isite_i,isite_j):
            distance[(isite_i,isite_j)]=(distance_,pattern_i,pattern_j)
        elif distance[(isite_i,isite_j)]>distance_:
            distance[(isite_i,isite_j)]=(distance_,pattern_i,pattern_j)
        cont+=1
    break


distance=[key+val for key,val in distance.items()]
import pandas as pd
disfile_colname=['isite_i','isite_j','distance','pattern_i','pattern_j']
distancedf=pd.DataFrame(distance,columns=disfile_colname)
distancedf.to_csv(dir1+'/ABW_selfdistance.csv')
