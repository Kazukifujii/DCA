from .clustermanager import ClusterManager
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist 
import polars as pl
import pandas as pd
import numpy as np
def cal_distances(cluster_manager: ClusterManager,reference=1e-8,target_atoms=['Si1','O1'],chunksize=10000):
        if cluster_manager.target_combination_df is None:
            cluster_manager.calculate_self_distance_file()
        target_files = pl.from_pandas(cluster_manager.target_combination_files)
        chunksize = chunksize if len(target_files) > chunksize else len(target_files)
        result = list()
        for fram in target_files.iter_slices(n_rows=chunksize):
            results_dis = np.empty(len(fram))
            target_cluster_coordinates = fram.select(
                        pl.all().apply(lambda file_i: pl.scan_csv(file_i))
                    )
            for pickup_atom in target_atoms:
                pickup_coordinates = target_cluster_coordinates.select(
                                pl.all().apply(lambda x: x.filter(pl.col('atom') == pickup_atom).select(['x', 'y', 'z']).collect().to_numpy())
                            )
                pickup_coordinates = pickup_coordinates.to_numpy()
                A = np.stack(pickup_coordinates[:,0],0)
                B = np.stack(pickup_coordinates[:,1],0)
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
                results_dis = np.sum(np.stack([results_dis,distance]),axis=0)
            results_dis = results_dis/len(target_atoms)
            results_dis = np.where(results_dis < reference , 0.0 , results_dis)
            results_dis = results_dis.tolist()
            result.extend(results_dis)
        return pd.concat([cluster_manager.target_combination_df, pd.DataFrame(result, columns=['distance'])], axis=1)