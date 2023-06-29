
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

        result_df = pd.DataFrame(result_data, columns=['cifid', 'address', 'isite']).drop_duplicates().sort_values(by=['cifid','isite']).reset_index(drop=True)
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