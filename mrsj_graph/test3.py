from crystal_emd.show import double_clusterplot,change

from glob import glob 
import pandas as pd
adress1='result/sort_volume_ciffiles_top_100/8000163/8000163_13_0.csv'
adress2='result/allzeorite/CZP/CZP_9_11.csv'
df=pd.read_csv(adress1,index_col=0)
df2=pd.read_csv(adress2,index_col=0)
from crystal_emd.read_info import clusterplot
#clusterplot(df2,show=True,save=False)
change(adress2,adress1,show=True,save=False)