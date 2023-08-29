import polars as pl
import numpy as np
import pandas as pd
import os
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
import glob
def cal_emd(A,B):
    if A.shape==B.shape:
        n = A.shape[1]
        # ユークリッド距離
        d = [cdist(ai, bi) for ai, bi in zip(A, B)]
        # 線形割当問題の解
        assignment = [linear_sum_assignment(di) for di in d]
        # コスト
        distance = np.array([di[assignmenti].sum() / n for di,assignmenti in zip(d, assignment)])
    else:
        distance = np.array([float('nan')]*A.shape[0])
    return distance
#データベースとクラスターとの距離を計算するクラスを作成する
class ClusterFeatureCalculator():
    def __init__(self, databasepath,target_atoms=['Si1','O1'],reference=1e-8):
        self.targets_atoms = target_atoms
        self.reference = reference
        database_files = glob.glob(os.path.join(databasepath,'*.csv'))
        #データベースを数値データに落とし込む
        database_dfs = [pl.scan_csv(file_i) for file_i in database_files]
        database_coordinates = dict()
        for target_atom in target_atoms:
            df_atoms = [df_i.filter(pl.col('atom')==target_atom).select(['x','y','z']) for df_i in database_dfs]
            df_atoms = pl.collect_all(df_atoms)
            database_coordinates[target_atom] = np.array([df_i.to_numpy() for df_i in df_atoms])
        self.database_coordinates = database_coordinates

        self.__cluster_length = {atom:val.shape for atom,val in self.database_coordinates.items()}

        #データベースのファイルパスを整理しておく
        database_path_df = pd.DataFrame(database_files,columns=['file_path'])
        database_path_df['address_i'] = database_path_df['file_path'].apply(lambda x: os.path.dirname(x))
        database_path_df['cifid_i'] = database_path_df['file_path'].apply(lambda x: os.path.basename(x).replace('.csv','').split('_')[0])
        database_path_df['isite_i'] = database_path_df['file_path'].apply(lambda x: os.path.basename(x).replace('.csv','').split('_')[1])
        database_path_df['pattern_i'] = database_path_df['file_path'].apply(lambda x: os.path.basename(x).replace('.csv','').split('_')[2])
        database_path_df.drop('file_path',axis=1,inplace=True)
        self.database_path_df = database_path_df
    

    def cluster_calculate_features(self,clusterpath):
        target_cluster = pd.read_csv(clusterpath)
        self.distances_df = self.database_path_df.copy()
        distances = list()
        target_coordinates = {key:target_cluster.query(f"atom == @key")[['x','y','z']].to_numpy() for key in self.targets_atoms}
        for target_atom,coordinate_shape in self.__cluster_length.items():
            target_cluster_coordinates = np.array([target_coordinates[target_atom]]*coordinate_shape[0])
            distance = cal_emd(target_cluster_coordinates,self.database_coordinates[target_atom])
            distances.append(distance)
        
        distances = np.sum(distances,axis=0)/len(self.targets_atoms)
        distances = np.where(distances < self.reference , 0.0 , distances)
        self.distances_df['distance'] = distances
        self.distances_df['address_j'] = os.path.dirname(clusterpath)
        self.distances_df['cifid_j'] = os.path.basename(clusterpath).replace('.csv','').split('_')[0]
        self.distances_df['isite_j'] = os.path.basename(clusterpath).replace('.csv','').split('_')[1]
        self.distances_df['pattern_j'] = os.path.basename(clusterpath).replace('.csv','').split('_')[2]

        return self.distances_df.sort_values('distance').reset_index(drop=True).loc[0,'distance']
from joblib import Parallel, delayed

class CrystalFeatureCalculator(ClusterFeatureCalculator):
    def __init__(self, databasepath, n_jobs=-1,method='mean'):
        self.n_jobs = n_jobs
        self.method = method
        super().__init__(databasepath)
    
    def process_target_cluster(self,target_cluster):
        features = self.cluster_calculate_features(target_cluster)
        self.distances_df.copy()
        return features,self.distances_df.copy()

    def calculate_features(self, crystalpath):
        target_clusters = glob.glob('{}/*_0.csv'.format(crystalpath))
        result = Parallel(n_jobs=self.n_jobs)(delayed(self.process_target_cluster)(target_cluster) for target_cluster in target_clusters)
        result,self.calculate_log = zip(*result)
        self.calculate_log = list(self.calculate_log)
        if self.method == 'mean':
            return np.mean(result, axis=0)
        elif self.method == 'max':
            return np.max(result)