from cmath import nan
import copy,os,glob,sys
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import pandas as pd



def make_self_clusering(dir):
    cwd=os.getcwd()
    os.chdir(dir)
    selfcsv=glob.glob('*self_distance.csv')[0]
    cifid=os.path.basename(dir)
    df=pd.read_csv(selfcsv,index_col=['isite_i','isite_j','pattern_i','pattern_j'])
    sortindex=list()
    alindex=list()
    for i,data in df.groupby(level=[0,1]):
        sortindex.append(data.sort_values('distance').iloc[0,0])
    matrixdf=pd.DataFrame()
    for index in sortindex:
        isite_i,isite_j,_,_=df[df.iloc[:,0]==index].index.to_list()[0]
        distance=df[df.iloc[:,0]==index].distance.values[0]
        matrixdf.at[isite_i,isite_j]=copy.deepcopy(distance)
        matrixdf.at[isite_j,isite_i]=copy.deepcopy(distance)
    matrixdf=matrixdf.fillna(0)
    print(matrixdf)
    matrixdf.to_csv('sort_self_distanc.csv')
    result1 = linkage(matrixdf, method = 'average')
    dendrogram(result1)
    plt.title("{}_self_clutering".format(cifid))
    plt.savefig("{}_self_clutering".format(cifid))
    os.chdir(cwd)


import subprocess
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod'))
cifdir = cifdir_.split('\n')
del cifdir[0]
for i in cifdir:
    make_self_clusering(i)