import pandas as pd

df=pd.read_csv('result/sort_volume_ciffiles_top_100/cifpoint')
df=df.dropna().sort_values(by='point')
