from cmath import nan
from distance_func import make_distance

dir1='result/cod/ABW'
dir2='result/cod/ACO'
import glob
import re
csvlist1=glob.glob(dir1+'/*csv')
csvlist2=glob.glob(dir2+'/*csv')
distance=dict()

for i in csvlist1:
    for j in csvlist2:
        isite_i,pattern_i=tuple(re.findall('(?=_)*\d{1,}',i))
        isite_j,pattern_j=tuple(re.findall('(?=_)*\d{1,}',j))
        distance_=make_distance(i,j)
        if distance[(isite_i,isite_j)]==nan:
            distance[(isite_i,isite_j)]=distance_
        elif distance[(isite_i,isite_j)]>distance_:
            distance[(isite_i,isite_j)]=distance_

print(distance)
