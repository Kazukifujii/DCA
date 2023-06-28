import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster

def make_inputdf_linkage(cluster_distance_df):
    grouped_df = cluster_distance_df.groupby(['cifid_i', 'cifid_j', 'isite_i', 'isite_j', 'pattern_i']).min()
    grouped_df = grouped_df.reset_index().sort_index(axis=1)
    grouped_df['id_set'] = grouped_df.apply(lambda x: sorted([f"{x['cifid_i']}_{x['isite_i']}", f"{x['cifid_j']}_{x['isite_j']}"]), axis=1)
    grouped_df = grouped_df.sort_values('id_set').reset_index(drop=True)
    id_set = grouped_df['id_set'].copy()
    grouped_df.drop('id_set', axis=1, inplace=True)
    return grouped_df, id_set

def make_clustering(cluster_distance_df, method='ward', fclusternum=2):
    sorted_distance_df, id_set = make_inputdf_linkage(cluster_distance_df)
    result = linkage(sorted_distance_df['distance'].values, method=method)
    
    # クラスタリングの結果をまとめる
    set_list = list(id_set.apply(lambda x: x[0]).unique())
    set_list.append(id_set.iloc[-1][-1])
    set_df = pd.DataFrame(set_list, columns=['tag'])
    set_df[['cifid', 'isite']] = set_df['tag'].str.split('_', expand=True)
    set_df.drop('tag', axis=1, inplace=True)
    
    result_ = [num for num in list(fcluster(result, fclusternum))]
    return pd.concat([set_df, pd.Series(result_, name='class')], axis=1)

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
        fdf=fdf.drop_duplicates(subset=['class'])
        fdf.drop(['class'],axis=1,inplace=True)
        fdf['address']=data['cifaddress']
        result.append(fdf)
        os.chdir(cwd)
    totalinfo=pd.concat(result)
    return totalinfo