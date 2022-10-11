from copy import deepcopy
import pandas as pd
import numpy as np
from crystal_emd.distance_func import cal_distance_df

def cal_r_t(clusterdf1,clsuterdf2):
    a=clusterdf1.loc[:,'x':'z'].values
    b=clsuterdf2.loc[:,'x':'z'].values
    c_a=np.mean(a,axis=0)
    c_b=np.mean(b,axis=0)
    a-=c_a
    b-=c_b
    h=np.dot(a.T,b)
    u,s,v=np.linalg.svd(h)
    #r=pd.DataFrame(np.dot(v.T,u.T))
    #t=pd.DataFrame(np.dot(-r,c_a)+c_b)
    r=np.dot(v.T,u.T)
    t=np.dot(-r,c_a)+c_b
    return r,t

class IterativeClosestPoint:
    def __init__(self,clusterdf1,clusterdf2):
        self.clusterdf1=deepcopy(clusterdf1)
        self.clusterdf2=deepcopy(clusterdf2)

    def stat_cal(self,calcont=1000):
        recal_clusterdf=deepcopy(self.clusterdf2)
        for i in range(calcont):
            r,t=cal_r_t(self.clusterdf1,recal_clusterdf)
            for i,data in recal_clusterdf.loc[:,'x':'z'].iterrows():
                recal_clusterdf.loc[i,'x':'z']=data.dot(r)+t
            distance=cal_distance_df(self.clusterdf1,recal_clusterdf)
            if distance<=10**(-8):
                break
        self.r,self.t=deepcopy(r),deepcopy(t)
        self.reccal_clusterdf=recal_clusterdf.copy()

"""
dir='result/allzeorite_tetrahedron/ABW'
df1=pd.read_csv('{}/ABW_0_0.csv'.format(dir),index_col=0)
df2=pd.read_csv('{}/ABW_0_9.csv'.format(dir),index_col=0)

icp=IterativeClosestPoint(df1,df2)
icp.stat_cal()
icp.reccal_clusterdf.to_csv('test.csv')
sys.exit()
from crystal_emd.show import change

csvn1='test.csv'
csvn2='{}/ABW_0_0.csv'.format(dir)
change(csvn1,csvn2)
"""