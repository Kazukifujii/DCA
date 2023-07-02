
import os
import glob
import re
import pandas as pd
from itertools import combinations
import polars as pl
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
        df_i = pl.from_pandas(self.cluster_list_df.iloc[[i[0] for i in combinations_list]].reset_index(drop=True))
        df_j = pl.from_pandas(self.cluster_list_df.iloc[[i[1] for i in combinations_list]].reset_index(drop=True))
        df_i.columns = ['cifid_i', 'address_i', 'isite_i']
        df_j.columns = ['cifid_j', 'address_j', 'isite_j']
        df = pl.concat([df_i, df_j],how='horizontal')
        target_combinations = []
        
        #クラスターのすべての回転パターンを作成する
        dim=len(df_i)
        for i in range(12):
            target_combinations.append(pl.concat([df,pl.DataFrame([i]*dim,schema = ['pattern_j'])],how='horizontal'))
        target_combination_df = pl.concat(target_combinations,how="vertical")
        target_combination_df = pl.concat([target_combination_df,pl.DataFrame([0]*target_combination_df.height,schema = ['pattern_i'])],how='horizontal')
        
        target_combination_files = target_combination_df.select(
                                    pl.concat_str([
                                        pl.col('address_i'),
                                        pl.concat_str([
                                            pl.concat_str([pl.col('cifid_i'),pl.col('isite_i'),pl.col('pattern_i')],separator='_'),    
                                            pl.lit('csv')],separator='.')]
                                    ,separator='/').alias('file_i'),
                                    
                                    pl.concat_str([
                                        pl.col('address_j'),
                                        pl.concat_str([
                                            pl.concat_str([pl.col('cifid_j'),pl.col('isite_j'),pl.col('pattern_j')],separator='_'),    
                                            pl.lit('csv')],separator='.')]
                                    ,separator='/').alias('file_j'),                 
                                    )
        self.target_combination_files = target_combination_files.to_pandas()
        self.target_combination_df = target_combination_df.to_pandas()