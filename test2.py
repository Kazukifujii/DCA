import pandas as pd
df=pd.read_csv('result/allzeorite_tetrahedron/ABW/ABW_0_0.csv',index_col=0)
df2=pd.read_csv('result/allzeorite_tetrahedron/ABW/ABW_6_0.csv',index_col=0)
from crystal_emd.read_info import cluster_match
print(cluster_match(df,df2))