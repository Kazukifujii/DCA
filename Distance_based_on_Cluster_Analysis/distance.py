from .clustermanager import ClusterManager
import torch
from .layers import SinkhornDistance    
import polars as pl
import pandas as pd
def cal_distances(cluster_manager: ClusterManager,reference=1e-8,eps=0.1, max_iter=1000,target_atoms=['Si1','O1'],chunksize=10000):
        #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        device = torch.device("cpu")
        if cluster_manager.target_combination_df is None:
            cluster_manager.calculate_self_distance_file()
        target_files = pl.from_pandas(cluster_manager.target_combination_files)
        sinkhorn = SinkhornDistance(eps=eps, max_iter=max_iter)
        chunksize = chunksize if len(target_files) > chunksize else len(target_files)
        result = list()
        for fram in target_files.iter_slices(n_rows=chunksize):
            results_dis = torch.zeros(len(fram),dtype=torch.float32)
            target_cluster_coordinates = fram.select(
                        pl.all().apply(lambda file_i: pl.scan_csv(file_i))
                    )
            for pickup_atom in target_atoms:
                pickup_coordinates = target_cluster_coordinates.select(
                                pl.all().apply(lambda x: x.filter(pl.col('atom') == pickup_atom).select(['x', 'y', 'z']).collect().to_numpy().tolist())
                            )
                pickup_coordinates = pickup_coordinates.to_numpy()
                A = torch.tensor(pickup_coordinates[:,0].tolist(),dtype=torch.float32)
                B = torch.tensor(pickup_coordinates[:,1].tolist(),dtype=torch.float32)
                #del pickup_coordinates
                distance, _, _ = sinkhorn(A, B)
                distance=torch.where(distance < reference, torch.tensor(0.0,device=device), distance)
                results_dis = torch.sum(torch.stack([results_dis,distance]),dim=0)
            results_dis = results_dis/len(target_atoms)
            results_dis = results_dis.cpu().numpy().tolist()
            result.extend(results_dis)
        return pd.concat([cluster_manager.target_combination_df, pd.DataFrame(result, columns=['distance'])], axis=1)