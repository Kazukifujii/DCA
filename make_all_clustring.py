import copy,os,glob,re,subprocess,math
import csv
from turtle import delay
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram,fcluster
import pandas as pd
from scipy.spatial.distance import squareform
from joblib import Parallel,delayed

def make_sort_distamce_(df,data):
    index=data.sort_values('distance').iloc[0,0]
    isite_i,isite_j,_,_=df[df.iloc[:,0]==index].index.to_list()[0]
    distance=df[df.iloc[:,0]==index].distance.values[0]
    if math.isclose(distance,0.0,abs_tol=0.05):
        distance=0.0
    return (isite_i,isite_j,copy.deepcopy(distance))



def make_sort_distance(selfcsv,csvn='sort_self_distanc.csv'):
    df=pd.read_csv(selfcsv,index_col=['isite_i','isite_j','pattern_i','pattern_j'])
    standdf_=list()
    """
    for i,data in df.groupby(level=[0,1]):
        index=data.sort_values('distance').iloc[0,0]
        isite_i,isite_j,_,_=df[df.iloc[:,0]==index].index.to_list()[0]
        distance=df[df.iloc[:,0]==index].distance.values[0]
        if math.isclose(distance,0.0,abs_tol=0.05):
            distance=0.0
        matrixdf.at[isite_i,isite_j]=copy.deepcopy(distance)
        matrixdf.at[isite_j,isite_i]=copy.deepcopy(distance)
        standdf_.append((isite_i,isite_j,copy.deepcopy(distance)))
    """
    standdf_=Parallel(n_jobs=6)(delayed(make_sort_distamce_)(df,data) for i,data in df.groupby(level=[0,1]))
    print('end sort distance')
    standdf=pd.DataFrame(standdf_,columns=['isite_i','isite_j','distance'])
    standdf.to_csv(csvn)
    matrixdf=pd.DataFrame(squareform(standdf.distance),index=list(set(standdf.isite_i.to_list()+standdf.isite_j.to_list())))
    matrixdf=matrixdf.sort_index()
    matrixdf=matrixdf.sort_index(axis=1)
    matrixdf.to_csv('matrix_{}'.format(csvn))
    return matrixdf

def make_all_clusering(csvn='sort_self_distanc.csv',pngn='cluster.png',method='single',fclusternum=0.0):
    selfcsv=glob.glob('all_distance.csv')[0]
    matrixdf=make_sort_distance(selfcsv,csvn)
    result=linkage(squareform(matrixdf), method = method)
    idx=matrixdf.index.to_list()
    dendrogram(result,labels=idx)
    plt.title(pngn)
    plt.savefig(pngn)
    plt.close()
    result_=[(idx[i],num) for i,num in enumerate(list(fcluster(result,fclusternum)))]
    return pd.DataFrame(result_,columns=['isite','fclusternum'])
"""
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/sorttest'))
cifdir = cifdir_.split('\n')
del cifdir[0]
"""

dir='/home/fujikazuki/crystal_emd/result/allzeorite'
cwd=os.getcwd()
os.chdir(dir)
result=make_all_clusering(csvn='all_sort_self_distanc.csv',pngn='all_self_cluster.png')
os.chdir(cwd)
import pickle
with open(("all_clustering_data.pickle"),"wb") as fwb:
    pickle.dump(result,fwb)

