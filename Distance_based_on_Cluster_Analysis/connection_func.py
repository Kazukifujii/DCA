from cmath import nan
from copy import deepcopy
import numpy as np
from Distance_based_on_Cluster_Analysis.distance_func import cal_distance_df
import math
def cal_r_t(clusterdf1,clsuterdf2):
    a=clusterdf1.loc[:,'x':'z'].values.astype(float)
    b=clsuterdf2.loc[:,'x':'z'].values.astype(float)
    c_a=np.mean(a,axis=0)
    c_b=np.mean(b,axis=0)
    a-=c_a
    b-=c_b
    h=np.dot(a.T,b)
    u,_,v=np.linalg.svd(h)
    r=np.dot(v.T,u.T)
    t=np.dot(-r,c_a)+c_b
    return r,t
from .show import DrawGif
class IterativeClosestPoint():
    def __init__(self,clusterdf1,clusterdf2):
        self.clusterdf1=deepcopy(clusterdf1)
        self.clusterdf2=deepcopy(clusterdf2)
        self.mgif=DrawGif()

    def start_cal(self,calcont=30,gif=False,gifname='icp.gif',convergence_val=10**(-8)):
        recal_clusterdf=deepcopy(self.clusterdf2)
        if gif:
            self.mgif.set_data(clusterdf1=self.clusterdf1,clusterdf2=recal_clusterdf)
        #print('\n i,distance')
        for i in range(calcont):
            r,t=cal_r_t(self.clusterdf1,recal_clusterdf)
            for j,data in recal_clusterdf.loc[:,'x':'z'].iterrows():
                recal_clusterdf.loc[j,'x':'z']=data.dot(r)-t
            distance=cal_distance_df(self.clusterdf1,recal_clusterdf)
            if gif:
                self.mgif.set_data(clusterdf1=self.clusterdf1,clusterdf2=recal_clusterdf)
            #print('\r{},{}'.format(i,distance),end='')
            if distance<=convergence_val:
                self.distance=deepcopy(distance)
                self.r,self.t=deepcopy(r),deepcopy(t)
                self.recal_clusterdf=recal_clusterdf.copy()
                if gif:
                    self.mgif.makegif(filename=gifname)
                return True
            elif math.isnan(distance):
                if gif:
                    self.mgif.makegif(filename=gifname)
                return False
        if gif:
            self.mgif.makegif(filename=gifname)
        return False
        
"""
dir='result/allzeorite_tetrahedron/ABW'
df1=pd.read_csv('{}/ABW_0_0.csv'.format(dir),index_col=0)
df2=pd.read_csv('{}/ABW_0_9.csv'.format(dir),index_col=0)

icp=IterativeClosestPoint(df1,df2)
icp.stat_cal()
icp.reccal_clusterdf.to_csv('test.csv')
sys.exit()
from Distance_based_on_Cluster_Analysis.show import change

csvn1='test.csv'
csvn2='{}/ABW_0_0.csv'.format(dir)
change(csvn1,csvn2)
"""