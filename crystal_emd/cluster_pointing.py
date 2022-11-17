from .cluster_adress_func import cluster_list
from .distance_func import parallel_self_distance
import time,re,os
import pandas as pd
from joblib import Parallel,delayed
from glob import glob


class make_cluster_point:
    def __init__(self,datasetadress):
        #self.datalist=cluster_list(datasetadress)
        self.datalist=cluster_list(datasetadress,dirs=len(glob('{}/*.csv'.format(datasetadress)))==0)
        self.datasetbasename=os.path.basename(datasetadress)
    def cal_cluster_point(self,clusteradress,n_job,outdir=False,method='average'):
        tstime=time.perf_counter()
        dirname=os.path.dirname(clusteradress)
        basename=os.path.basename(clusteradress)
        isite=int(re.split('_',basename)[-2])
        cifid=re.sub('_[0-9]*_[0-9]*\.csv','',basename)
        datalist_=pd.DataFrame([cifid,dirname,isite],index=self.datalist.columns.to_list())
        datalist_=pd.concat([self.datalist,datalist_.T],ignore_index=True)
        comb=[(datalist_.index.to_list()[-1],i) for i in datalist_.index.to_list()[0:-1]]
        plist=[i for i in range(12)]
        alllen=12
        cont=0
        distance=list()
        for pi in plist:
            cont+=1
            print("\r"+str(cont)+'/'+str(alllen),end="")
            fstime=time.perf_counter()
            distance_=Parallel(n_jobs=n_job)(delayed(parallel_self_distance)(datalist_,comb_,pi,method) for comb_ in comb)
            distance+=distance_
            etiem=time.perf_counter()
            #print('\r\ncomputation time {}'.format(etiem-fstime))
        disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
        self.distancedf=pd.DataFrame(distance,columns=disfile_colname).sort_values(by='distance')
        self.distancedf.to_csv('{}/{}_{}.distance'.format(dirname,basename.replace('.csv',''),os.path.basename(self.datasetbasename)))
        print('total computation time {}'.format(etiem-tstime))
        self.cluster_point=self.distancedf.iloc[0].distance


class make_crystall_point(make_cluster_point):
    def __init__(self,datasetadress):
        super().__init__(datasetadress)
    def cal_crystal_point(self,cifdiradress,n_job=6,method='average'):
        self.crystal_point=float()
        for i,data in cluster_list(cifdiradress).iterrows():
            clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
            self.cal_cluster_point(clusteradress, n_job=n_job,method=method)
            self.crystal_point+=self.cluster_point