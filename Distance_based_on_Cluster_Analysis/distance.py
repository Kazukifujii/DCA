from .clustermanager import ClusterManager
import torch
import pandas as pd
from .layers import SinkhornDistance
def cal_distances(cluster_manager: ClusterManager,reference=1e-8,eps=0.1, max_iter=1000):
    if cluster_manager.target_combination_df is None:
        cluster_manager.calculate_self_distance_file()

    target_files = cluster_manager.target_combination_files.copy()
    target_cluster_coordinates = target_files.applymap(lambda x: pd.read_csv(x, index_col=0))

    target_atoms = target_cluster_coordinates.applymap(lambda x: set(x.loc[:, 'atom'].unique().tolist()))
    target_atoms = target_atoms.apply(lambda x: set.union(*x.values.tolist()), axis=1)
    target_atoms = set.union(*target_atoms.values.tolist())

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    results = dict()

    sinkhorn = SinkhornDistance(eps=eps, max_iter=max_iter)
    sinkhorn.to(device)
    for pickup_atom in target_atoms:
        pickup_coordinates = target_cluster_coordinates.applymap(lambda x: x.loc[x.loc[:, 'atom'] == pickup_atom, ['x', 'y', 'z']].to_numpy().tolist())
        A = torch.tensor(pickup_coordinates.iloc[:, 0].values.tolist(), device=device)
        B = torch.tensor(pickup_coordinates.iloc[:, 1].values.tolist(),device=device)
        distance, _, _ = sinkhorn(A, B)
        distance=torch.where(distance < reference, torch.tensor(0.0), distance)
        distance=distance.cpu().numpy()
        results[pickup_atom]= distance
    results=pd.DataFrame(results).mean(axis=1)
    results.name='distance'
    return pd.concat([cluster_manager.target_combination_df,results],axis=1)

