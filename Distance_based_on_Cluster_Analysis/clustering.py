import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster

def make_inputdf_linkage(cluster_distance_df):
    grouped_df = cluster_distance_df.groupby(['cifid_i', 'cifid_j','isite_i','isite_j','pattern_i']).apply(lambda x: x.sort_values(['distance'], ascending=True).iloc[0,:])
    grouped_df = grouped_df.reset_index(drop=True)
    return grouped_df

def make_clustering(cluster_distance_df, method='single', fclusternum=0.0):
    sorted_distance_df = make_inputdf_linkage(cluster_distance_df)
    result = linkage(sorted_distance_df['distance'].values, method=method)
    
    # ラベル付け
    result_ = [num for num in list(fcluster(result, fclusternum))]
    
    # クラスタリングの結果をまとめる
    data_i=sorted_distance_df.loc[:,sorted_distance_df.columns.str.contains('_i')].drop_duplicates()
    data_j=sorted_distance_df.loc[:,sorted_distance_df.columns.str.contains('_j')].drop_duplicates()
    tagsdf=pd.DataFrame(data_i.apply(lambda x: f'{x.cifid_i}_{x.isite_i}',axis=1).to_list()+data_j.apply(lambda x: f'{x.cifid_j}_{x.isite_j}',axis=1).to_list()[-1:],columns=['tag'])
    tagsdf[['cifid', 'isite']] = tagsdf['tag'].str.split('_', expand=True)
    tagsdf.drop('tag', axis=1, inplace=True)
    result_df = pd.DataFrame(result_, columns=['Class'])
    
    return pd.concat([tagsdf, result_df], axis=1)

import os,glob
def fcluster_list(info):
    cwd=os.getcwd()
    result=list()
    for i in range(len(info)):
        data=info.iloc[i,:]
        os.chdir(data['cifaddress'])
        try:
            csvn=glob.glob('*_fcluster.csv')[0]
        except:
            print('no such file')
            os.chdir(cwd)
            continue
        fdf=pd.read_csv(csvn,index_col=0)
        fdf=fdf.drop_duplicates(subset=['Class'])
        fdf.drop(['Class'],axis=1,inplace=True)
        fdf['address']=data['cifaddress']
        result.append(fdf)
        os.chdir(cwd)
    totalinfo=pd.concat(result)
    return totalinfo