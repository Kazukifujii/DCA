import copy,os,glob
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import pandas as pd
import math
from scipy.cluster.hierarchy import ClusterWarning
from warnings import simplefilter
import copy

def make_sort_distance(selfcsv,csvn='sort_self_distanc.csv'):
    df=pd.read_csv(selfcsv,index_col=['isite_i','isite_j','pattern_i','pattern_j'])
    sortindex=list()
    for i,data in df.groupby(level=[0,1]):
        sortindex.append(data.sort_values('distance').iloc[0,0])
    matrixdf=pd.DataFrame()
    standdf_=list()
    for index in sortindex:
        isite_i,isite_j,_,_=df[df.iloc[:,0]==index].index.to_list()[0]
        distance=df[df.iloc[:,0]==index].distance.values[0]
        if math.isclose(distance,0.0,abs_tol=0.05):
            distance=0.0
        matrixdf.at[isite_i,isite_j]=copy.deepcopy(distance)
        matrixdf.at[isite_j,isite_i]=copy.deepcopy(distance)
        standdf_.append((isite_i,isite_j,copy.deepcopy(distance)))
    matrixdf=matrixdf.fillna(0)
    matrixdf=matrixdf.sort_index()
    matrixdf=matrixdf.sort_index(axis=1)
    standdf=pd.DataFrame(standdf_,columns=['isite_i','isite_j','distance'])
    standdf.to_csv(csvn)
    return matrixdf

def make_self_clusering(dir,csvn='sort_self_distanc.csv',pngn='cluster.png',method='ward'):
    cwd=os.getcwd()
    os.chdir(dir)
    selfcsv=glob.glob('*self_distance.csv')[0]
    matrixdf=make_sort_distance(selfcsv,csvn)
    from scipy.spatial.distance import squareform
    result1 = linkage(squareform(matrixdf), method = method)
    dendrogram(result1,labels=matrixdf.index.to_list())
    plt.title(pngn)
    plt.savefig(pngn)
    plt.close()
    os.chdir(cwd)


import subprocess
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/sorttest'))
cifdir = cifdir_.split('\n')
del cifdir[0]
import re
for i in cifdir:
    cifid=re.split('/',i)[-1]
    print(cifid)
    make_self_clusering(i,csvn='{}_sort_self_distanc.csv'.format(cifid),pngn='{}_self_cluster.png'.format(cifid))