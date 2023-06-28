import copy,os,glob,re
import pandas as pd
import subprocess
import re
def fcluster_list(dir):
    if os.path.isfile('{}/target_dirs.csv'.format(dir)):
        cifdirs=pd.read_csv('{}/target_dirs.csv'.format(dir),index_col=0).cifaddress.to_list()
    else:
        cifdirs= subprocess.getoutput("find {0} -type d | sort".format(dir))
        cifdirs= cifdirs.split('\n')
        del cifdirs[0]
    picinfo=list()
    cwd=os.getcwd()
    for _,cifdir in enumerate(cifdirs):
        cifid=re.split('/',cifdir)[-1]
        print(cifid)
        os.chdir(cifdir)
        try:
            csvn=glob.glob('*fcluster*')[0]
        except:
            print('no such file')
            os.chdir(cwd)
            continue
        info=pd.read_csv(csvn,index_col=0)
        picisite=copy.deepcopy(info.iloc[info.fclusternum.drop_duplicates().index].isite.values)
        picisite=[re.split("_", picisite_)[1] for picisite_ in picisite]
        picinfo_=[(cifid,cifdir,isite) for isite in picisite]
        picinfo+=picinfo_
        os.chdir(cwd)

    totalinfo=pd.DataFrame(picinfo,columns=['cifid','address','isite'])
    totalinfo.to_csv('{}/target_cluster_files.csv'.format(dir))
    return totalinfo

"""def isite_list(dir):
    #for i,address in enumerate(csvlist):
    cifid=re.split('/',dir)[-1]
    ciflist=glob.glob('{}/{}_[0-9]*.csv'.format(dir,cifid))
    isitelist=[re.split('_',csvname)[-2] for csvname in ciflist]
    isitelist=list(set(isitelist))
    isitelist=[int(isitelist_) for isitelist_ in isitelist]
    isitelist.sort()
    picinfo=[(('{}').format(cifid),dir,isite) for isite in isitelist]
    resultdf=pd.DataFrame(picinfo,columns=['cifid','address','isite'])
    resultdf.to_csv('{}/isite_list'.format(dir))
    return resultdf"""

def cluster_list(dir, dirs=False):
    clusterlist = glob.glob('{}/*/*_[0-9]*.csv'.format(dir)) if dirs else glob.glob('{}/*_[0-9]*.csv'.format(dir))
    result_data = []

    for filepath in clusterlist:
        filename = os.path.basename(filepath)
        dirname = os.path.dirname(filepath)
        cifid, isite, _ = tuple(re.split('_', filename))
        result_data.append((cifid, dirname, int(isite)))

    resultdf = pd.DataFrame(result_data, columns=['cifid', 'address', 'isite']).drop_duplicates().sort_values(by='cifid').reset_index(drop=True)
    return resultdf


import os
import glob
import re
import pandas as pd
from itertools import combinations

class ClusterManager:
    def __init__(self, cluster_list_df):
        self.cluster_list_df = cluster_list_df
        self.target_combination_df = None
    @classmethod
    def from_dirpath(cls, dirpath, dirs=False):
        cluster_list_df = cls.read_cluster_list(dirpath, dirs)
        return cls(cluster_list_df)
    
    @staticmethod
    def read_cluster_list(dirpath, dirs):
        cluster_list = glob.glob('{}/*/*_[0-9]*.csv'.format(dirpath)) if dirs else glob.glob('{}/*_[0-9]*.csv'.format(dirpath))
        result_data = []

        for filepath in cluster_list:
            filename = os.path.basename(filepath)
            dirname = os.path.dirname(filepath)
            cifid, isite, _ = tuple(re.split('_', filename))
            result_data.append((cifid, dirname, int(isite)))

        result_df = pd.DataFrame(result_data, columns=['cifid', 'address', 'isite']).drop_duplicates().sort_values(by='cifid').reset_index(drop=True)
        return result_df
    
    def calculate_self_distance_file(self):
        combinations_list = list(combinations(range(len(self.cluster_list_df)), 2))
        df_i = self.cluster_list_df.iloc[[i[0] for i in combinations_list]].reset_index(drop=True)
        df_j = self.cluster_list_df.iloc[[i[1] for i in combinations_list]].reset_index(drop=True)
        df_i.columns = ['cifid_i', 'address_i', 'isite_i']
        df_j.columns = ['cifid_j', 'address_j', 'isite_j']
        
        target_combinations = []

        #クラスターのすべての回転パターンを作成する
        dim=len(df_i)
        for i in range(12):
            target_combinations.append(pd.concat([df_i, df_j,pd.Series([i]*dim,name='pattern_j')], axis=1))
        target_combination_df = pd.concat(target_combinations, ignore_index=True).sort_index(axis=1)
        target_combination_df['pattern_i'] = 0
        
        self.target_combination_df = target_combination_df
        self.target_combination_files = pd.DataFrame()
        self.target_combination_files['file_i'] = self.target_combination_df.apply(lambda x: os.path.join(x['address_i'], f"{x['cifid_i']}_{x['isite_i']}_{x['pattern_i']}.csv"), axis=1)
        self.target_combination_files['file_j'] = self.target_combination_df.apply(lambda x: os.path.join(x['address_j'], f"{x['cifid_j']}_{x['isite_j']}_{x['pattern_j']}.csv"), axis=1)