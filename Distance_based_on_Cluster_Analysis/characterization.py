import polars as pl
import numpy as np
import pandas as pd
import os
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
import glob
from itertools import product

def cal_emd(A:np.array,B:np.array) -> np.array:
    #A,B:原子の座標
    #A,Bは共にm*n*3の配列である必要がある
    if A.shape==B.shape:
        #原点を除く原子の個数
        n = A.shape[1]-1 if (A[0,:]==0).all() else A.shape[1]
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
def tilda(u):
    return np.array([[0,-u[2],u[1]],[u[2],0,-u[0]],[-u[1],u[0],0]])

def make_inertia_matrix(cluster_coordinate:np.ndarray) -> np.ndarray:
    cluster_coordinate_tilda = np.array([tilda(u) for u in cluster_coordinate])
    inertia_matrixs = -np.array([np.dot(tilda_vec, tilda_vec) for tilda_vec in cluster_coordinate_tilda]) 
    return np.sum(inertia_matrixs,axis=0)

def cal_eigenvalues(cluster_coordinate:np.ndarray) -> list():
    inertia_matrix = make_inertia_matrix(cluster_coordinate)
    eigenvalues, _ = np.linalg.eig(inertia_matrix)
    return sorted(eigenvalues.real)

def _cal_distance(target_coords,database_coords):
    distances = list()
    for target_atom,database_coord in database_coords.items():
        target_cluster_coordinates = np.array([target_coords[target_atom]]*database_coord.shape[0])
        distance = cal_emd(target_cluster_coordinates,database_coord)
        distances.append(distance)
    distances = np.sum(distances,axis=0)/len(['Si1','O1'])
    distances = np.where(distances < 1e-8 , 0.0 , distances)
    return distances

class ClusterFeatureCalculator():
    def __init__(self, databasepath,target_atoms=['Si1','O1'],reference=1e-8,sep_value=0.1,offset=5,eig_max_neiber_num=2,use_mesh_flag=True):
        self.targets_atoms = target_atoms
        self.sep_value = sep_value
        self.offset = offset
        self.use_mesh_flag = use_mesh_flag

        database_files = glob.glob(os.path.join(databasepath,'*.csv'))
        
        #固有値を求め、ファイルリストのインデックスにキーを割り当てる

        #データベースに保存されているクラスターのデータを特定の隣接数以下でフィルタリングする
        self.eig_max_neiber_num = eig_max_neiber_num
        database_dfs = [pl.scan_csv(file_i) for file_i in database_files]
        database_dfs = [df_i.filter(pl.col('neighbor_num')<=self.eig_max_neiber_num).select(pl.col(['x','y','z'])) for df_i in database_dfs]
        #numpy型で数値データに変換する
        database_dfs = pl.collect_all(database_dfs)
        database_coordinates = [df_i.to_numpy() for df_i in database_dfs]

        #モーメントの固有値の計算を行う
        eigs = [cal_eigenvalues(cluster_coordinate) for cluster_coordinate in database_coordinates]
        
        #データベースのファイルパスとそれに対応する固有値を整理し保存する
        database_path_df = pl.LazyFrame({'file_path':database_files,'eigs':eigs})
        database_path_df = database_path_df.with_columns(
            pl.col("file_path").map_elements(os.path.dirname).alias("address_i"),
            pl.col("file_path").map_elements(lambda x: os.path.basename(x).replace('.csv', '').split('_')[0]).alias("cifid_i"),
            pl.col("file_path").map_elements(lambda x: os.path.basename(x).replace('.csv', '').split('_')[1]).alias("isite_i"),
            pl.col("file_path").map_elements(lambda x: os.path.basename(x).replace('.csv', '').split('_')[2]).alias("pattern_i"),
            pl.col("eigs").list.get(0).alias("eig_1"),
            pl.col("eigs").list.get(1).alias("eig_2"),
            pl.col("eigs").list.get(2).alias("eig_3")
        ).select(pl.col(['address_i','cifid_i','isite_i','pattern_i','eig_1','eig_2','eig_3']))
        

        sep_value = str(sep_value)
        #固有値の情報をもとにクラスターを分類する
        database_path_df = database_path_df.with_columns(
        (pl.col('eig_1')//self.sep_value).cast(int).alias("eig_1_mesh"),
        (pl.col('eig_2')//self.sep_value).cast(int).alias("eig_2_mesh"),
        (pl.col('eig_3')//self.sep_value).cast(int).alias("eig_3_mesh")
        )

        self.database_path_df = database_path_df.collect().to_pandas()

        #メッシュの検索を行うための辞書を作成
        self.database_mesh_dict = self.database_path_df.groupby(['eig_1_mesh', 'eig_2_mesh', 'eig_3_mesh']).apply(lambda x:x.index.tolist()).to_dict()

        #計算用のcluster_coordinateを作成する
        self.reference = reference
        #データベースを数値データに落とし込む
        database_dfs = [pl.scan_csv(file_i) for file_i in database_files]
        database_coordinates = dict()
        for target_atom in target_atoms:
            df_atoms = [df_i.filter(pl.col('atom')==target_atom).select(['x','y','z']) for df_i in database_dfs]
            df_atoms = pl.collect_all(df_atoms)
            database_coordinates[target_atom] = np.array([df_i.to_numpy() for df_i in df_atoms])
        self.database_coordinates = database_coordinates

        #ログフォーマットの作成
        self.log_format = self.database_path_df.drop(['eig_1', 'eig_2','eig_3', 'eig_1_mesh', 'eig_2_mesh', 'eig_3_mesh'], axis=1).copy()


    def change_offset(self,offset):
        self.offset = offset
    
    def change_sep_value(self,sep_value):
        self.sep_value = sep_value
    
    def change_use_mesh_flag(self,use_mesh_flag):
        self.use_mesh_flag = use_mesh_flag

    def _cal_mesh(self,target_cluster:pd.DataFrame):
        #target_clusterのモーメントの固有値を求める
        target_eigs = sorted(cal_eigenvalues(target_cluster.query(f'neighbor_num<={self.eig_max_neiber_num}')[['x','y','z']].to_numpy()))
        target_eigs = np.array(target_eigs)
        return (target_eigs//self.sep_value).astype(int)
    
    def _make_query_keys(self,mesh):
        mesh_lenge = [i for i in range(-self.offset,self.offset+1)]
        offsets = product(*[mesh_lenge] * 3)
        target_cells = [tuple(mesh + offset) for offset in offsets]
        return target_cells
    
    def _get_target_databse_indexs(self,querys):
        return [i for  query in querys if query in self.database_mesh_dict.keys() for i in self.database_mesh_dict[query]]

    def cluster_calculate_features(self,clusterpath):
        #clusterpath:クラスターのファイルパス

        target_cluster = pd.read_csv(clusterpath,index_col=0)
        #target_clusterのモーメントの固有値を求める
        target_mesh = self._cal_mesh(target_cluster)

        #計算対象のメッシュをリストアップ,offsetsは計算対象のメッシュの周囲
        querys = self._make_query_keys(target_mesh)

        #計算対象のメッシュの周囲のクラスターの特徴量を取得する
        if self.use_mesh_flag:
            target_database_indexs = self._get_target_databse_indexs(querys)
        else:
            target_database_indexs = self.database_path_df.index.tolist()

        #計算対象のクラスターの特徴量を取得する
        target_database_coordinates = {key:val[target_database_indexs] for key,val in self.database_coordinates.items()}
        target_coordinates = {key:target_cluster.query(f"atom == @key")[['x','y','z']].to_numpy() for key in self.targets_atoms}
        dis = _cal_distance(target_coordinates,target_database_coordinates)

        if len(dis) == 0:
            #計算対象のクラスターがデータベースに存在しない場合
            self.distances_df = 'no match'
            return np.nan
        self.distances_df = self.log_format.loc[target_database_indexs].copy()
        self.distances_df['distance'] = dis
        return dis.min()

class CrystalFeatureCalculator(ClusterFeatureCalculator):
    def __init__(self, databasepath,method='mean',target_atoms=['Si1','O1'],reference=1e-8,sep_value=0.1,offset=5,eig_max_neiber_num=2,use_mesh_flag=True):
        self.method = method
        super().__init__(databasepath,target_atoms,reference,sep_value,offset,eig_max_neiber_num,use_mesh_flag)
    
    def process_target_cluster(self,target_cluster):
        features = self.cluster_calculate_features(target_cluster)
        return features,self.distances_df

    def calculate_features(self, crystalpath):
        target_clusters = glob.glob('{}/*_0.csv'.format(crystalpath))
        result = [self.process_target_cluster(target_cluster) for target_cluster in target_clusters]
        result,self.calculate_log = zip(*result)
        self.calculate_log = list(self.calculate_log)
        if self.method == 'mean':
            return np.mean(result, axis=0)
        elif self.method == 'max':
            return np.max(result)