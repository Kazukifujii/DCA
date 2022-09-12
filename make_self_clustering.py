import copy,os,glob,re,math,subprocess
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram,fcluster
import pandas as pd
from scipy.spatial.distance import squareform


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

def make_self_clusering_(csvn='sort_self_distanc.csv',pngn='cluster.png',method='single',fclusternum=0.0):
    selfcsv=glob.glob('*self_distance.csv')[0]
    matrixdf=make_sort_distance(selfcsv,csvn)
    result=linkage(squareform(matrixdf), method = method)
    idx=matrixdf.index.to_list()
    dendrogram(result,labels=idx)
    plt.title(pngn)
    plt.savefig(pngn)
    plt.close()
    result_=[(idx[i],num) for i,num in enumerate(list(fcluster(result,fclusternum)))]
    return pd.DataFrame(result_,columns=['isite','fclusternum'])



def make_self_clusering(dir):
    if os.path.isfile('{}/picupadress'.format(dir)):
        cifdirs=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
    else:
        cifdirs= subprocess.getoutput("find {0} -type d | sort".format(dir))
        cifdirs= cifdirs.split('\n')
        del cifdirs[0]
    cwd=os.getcwd()
    fclusternum=0.0
    for i in cifdirs:
        cifid=re.split('/',i)[-1]
        try:
            print(cifid)
            os.chdir(i)
            result=make_self_clusering_(csvn='{}_sort_self_distanc.csv'.format(cifid),pngn='{}_self_cluster.png'.format(cifid),fclusternum=fclusternum)
            result.to_csv('{}_fclusternum={}'.format(cifid,str(fclusternum)))
            os.chdir(cwd)
        except:
            print('{} no such file'.format(cifid))
