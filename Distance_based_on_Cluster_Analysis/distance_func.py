from cmath import nan
from copy import deepcopy
import pandas as pd
import os,itertools,time,pulp
from joblib import Parallel,delayed

def calcost(data1,data2):
    data1c=data1.loc['x':'z']
    data2c=data2.loc['x':'z']
    redata=data1c-data2c
    if data1.atom==data2.atom:
        return redata.x**2+redata.y**2+redata.z**2
    return 1000

def cal_distance_df(cluster_df1,cluster_df2,values=False,histgram=False,method='average',pair_atoms=False):
    cluster1=deepcopy(cluster_df1)
    cluster2=deepcopy(cluster_df2)
    #make cost and constrains
    costs=dict()
    for i,data1 in cluster1.iterrows():
        for j,data2 in cluster2.iterrows():
            cost=calcost(data1,data2)
            costs[(i,j)]=cost
    
    model=pulp.LpProblem('cluster_matching',pulp.LpMinimize)
    f=dict()
    obfunc=list()
    for index,cost in costs.items():
        i,j=index
        f[i,j]=pulp.LpVariable('index{}_{}'.format(i,j),lowBound=0)
        obfunc.append(f[i,j]*cost)
    model+=pulp.lpSum(obfunc)

    for i,data1 in cluster1.iterrows():
        model += pulp.lpSum([f[(i,j)] for j,_ in cluster2.iterrows()])==1

    for j,data2 in cluster2.iterrows():
        model+= pulp.lpSum([f[(i,j)] for i,_ in cluster1.iterrows()])==1

    result=model.solve(pulp.PULP_CBC_CMD(msg = False))
    
    if result==1:
        if values:
            val=list()
            for var_ in f.values():
                if var_.varValue!=0:
                    val.append((str(var_),float(var_.varValue)))
            return val
        if histgram:
            hist=list()
            for key,var_ in f.items():
                if var_.varValue!=0:
                    hist.append(var_.varValue*pow(costs[key],0.5))
            return hist
        if pair_atoms:
            pairlist=list()
            for key,var_ in f.items():
                if var_.varValue!=0:
                    site1='{}_{}'.format(cluster1.loc[key[0]].atom,cluster1.loc[key[0]].isite)
                    site2='{}_{}'.format(cluster2.loc[key[1]].atom,cluster2.loc[key[1]].isite)
                    pairlist.append((site1,site2))
            return pairlist
        dis_=float()
        sumf=float()
        if method=='average':
            for val in f.values():
                sumf+=val.varValue
            for key,val in f.items():
                dis_+=val.varValue*pow(costs[key],0.5)
            return dis_/sumf
        elif method=='max':
            hist=list()
            for key,var_ in f.items():
                if var_.varValue!=0:
                    hist.append(var_.varValue*pow(costs[key],0.5))
            return max(hist)
    else:
        return nan


def cal_distance(csv_address1,csv_address2,values=False,histgram=False,method='average',pair_atoms=False):
    cluster1=pd.read_csv(csv_address1,index_col=0)
    cluster2=pd.read_csv(csv_address2,index_col=0)
    return cal_distance_df(cluster_df1=cluster1,cluster_df2=cluster2,values=values,histgram=histgram,method=method,pair_atoms=pair_atoms)

def parallel_self_distance(cluster_df,comb,pattern_j,method='average'):
    index_i,index_j=comb
    data_i=cluster_df.loc[index_i]
    data_j=cluster_df.loc[index_j]
    csvi='{}/{}_{}_0.csv'.format(data_i.address,data_i.cifid,data_i.isite,0)
    csvj='{}/{}_{}_{}.csv'.format(data_j.address,data_j.cifid,data_j.isite,pattern_j)
    if not (os.path.isfile(csvi) and os.path.isfile(csvj)):
        return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,nan)
    disij=cal_distance(csvi,csvj,method=method)
    return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,disij)

def make_distance_csv(listaddress,resultname,outdir=False):
    tstime=time.perf_counter()
    if type(listaddress) is str:
        all_cluster=pd.read_csv(listaddress,index_col=0)
    elif type(listaddress) is pd.DataFrame:
        all_cluster=listaddress
    else:
        print('make_distance_csv error')
    all_index=all_cluster.index.to_list()
    comb=list(itertools.combinations(all_index,2))
    plist=[i for i in range(12)]
    alllen=12
    cont=0
    distance=list()
    for pi in plist:
        cont+=1
        print("\r"+str(cont)+'/'+str(alllen),end="")
        fstime=time.perf_counter()
        distance_=Parallel(n_jobs=-1)(delayed(parallel_self_distance)(all_cluster,comb_,pi) for comb_ in comb)
        distance+=distance_
        etiem=time.perf_counter()
        #print('\r\ncomputation time {}'.format(etiem-fstime))
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    if outdir:
        distancedf.to_csv('{}/{}'.format(outdir,resultname))
    else:
        distancedf.to_csv('{}'.format(resultname))
    print()
    print('output {}'.format(resultname))
    print('total computation time {}'.format(etiem-tstime))

def remake_distance(distanceaddress,resultname=True,error_val=10**-8):
    if resultname:
        diraddress=os.path.dirname(distanceaddress)
        basename=os.path.basename(distanceaddress).replace('.csv','')
        if len(diraddress)==0:
            resultname='{}_remake'.format(basename)
        else:
            resultname='{}/{}_remake'.format(diraddress,basename)
    distancedf=pd.read_csv(distanceaddress,index_col=0)
    distancedf.loc[(distancedf.distance<=error_val),'distance']=0.0
    distancedf.to_csv(resultname)
    return