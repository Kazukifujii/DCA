import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import os 
import glob
import sys
import pandas as pd
cwd=os.getcwd()

dir=cwd+'/crystal_emd/result/cod/ABW/'
os.chdir(dir)
print(os.getcwd())
selfcsv=glob.glob('*self_distance.csv')[0]

df=pd.read_csv(selfcsv,index_col=0)

machingid=list()
for _,data in df.iterrows():
    tupleid=str(data.iloc[0:4].astype(int).values)
    machingid.append(((tupleid),data.distance))

clusteringdf=pd.DataFrame(machingid,columns=['id','distance']).set_index('id')

result1 = linkage(clusteringdf, method = 'weighted')
dendrogram(result1)
print(result1)

sys.exit()

plt.title("ABW_self_distance")
plt.ylabel("Threshold")
plt.show()