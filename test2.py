from crystal_emd.clustering_func import make_clusering

filen='cluster_dataset/OFF/OFF_self_distance'
import pandas as pd

df=pd.read_csv(filen,index_col=0)
df=make_clusering(filen)