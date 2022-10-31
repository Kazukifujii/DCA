import copy,os
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram,fcluster
import pandas as pd
from scipy.spatial.distance import squareform
from joblib import Parallel,delayed

def make_sort_distamce_(df,data):
    index=data.sort_values('distance').iloc[0,0]
    isite_i,isite_j,_,_=df[df.iloc[:,0]==index].index.to_list()[0]
    distance=df[df.iloc[:,0]==index].distance.values[0]
    """
    if math.isclose(distance,0.0,abs_tol=0.05):
        distance=0.0
    """
    return (isite_i,isite_j,copy.deepcopy(distance))

def make_sort_distance(selfcsv,csvn='sort_distanc.csv'):
    df=pd.read_csv(selfcsv,index_col=['isite_i','isite_j','pattern_i','pattern_j'])
    standdf_=list()
    standdf_=Parallel(n_jobs=-1)(delayed(make_sort_distamce_)(df,data) for i,data in df.groupby(level=[0,1]))
    standdf=pd.DataFrame(standdf_,columns=['isite_i','isite_j','distance'])
    standdf.to_csv(csvn)
    matrixdf=pd.DataFrame()
    for i,data in standdf.iterrows():
        matrixdf.at[data.isite_i,data.isite_j]=copy.deepcopy(data.distance)
        matrixdf.at[data.isite_j,data.isite_i]=copy.deepcopy(data.distance)
    matrixdf=matrixdf.sort_index()
    matrixdf=matrixdf.sort_index(axis=1)
    for dig in matrixdf.index.to_list():
        matrixdf.loc[dig,dig]=0
    matrixdf.dropna(inplace=True,how='all')
    matrixdf.dropna(inplace=True,axis=1,how='all')
    #matrixdf.to_csv('{}/matrix_{}'.format(os.path.dirname(csvn),os.path.basename(csvn)))
    return matrixdf

def make_clusering(csvadress,csvn='sort_distance.csv',pngn='cluster.png',method='single',fclusternum=0.0,cal_matrixdf=True):
    if cal_matrixdf:
        matrixdf=make_sort_distance(csvadress,csvn)
    else:
        matrixdf=pd.read_csv(csvadress,index_col=0)
    result=linkage(squareform(matrixdf), method = method)
    idx=matrixdf.index.to_list()
    dendrogram(result,labels=idx)
    #plt.title(pngn)
    plt.ylim(0,0.1)
    plt.xlim(0,800)
    plt.ylabel("angstrom")
    plt.savefig(pngn)
    plt.close()
    result_=[(idx[i],num) for i,num in enumerate(list(fcluster(result,fclusternum)))]
    return pd.DataFrame(result_,columns=['isite','fclusternum'])