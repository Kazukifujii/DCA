from cProfile import label
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import os 
import glob
import sys
import pandas as pd
cwd=os.getcwd()

dir=cwd+'/result/cod/ABW/'

os.chdir(dir)

selfcsv=glob.glob('*self_distance.csv')[0]

df=pd.read_csv(selfcsv,index_col=0)

machingid=list()
for _,data in df.iterrows():
    tupleid=str(data.iloc[0:4].astype(int).values)
    machingid.append(((tupleid),data.distance))

clusteringdf=pd.DataFrame(machingid,columns=['id','distance']).set_index('id')

result1 = linkage(clusteringdf, method = 'single')
dendrogram(result1,p=20,truncate_mode='lastp',labels=clusteringdf.index.to_list())

plt.title("ABW_self_distance")
plt.ylabel("Threshold")
plt.show()
os.chdir(cwd)