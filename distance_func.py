from cmath import  nan
import pandas as pd
import pulp

def calcost(data1,data2):
    data1c=data1.loc['x':'z']
    data2c=data2.loc['x':'z']
    redata=data1c-data2c
    if data1.atom==data2.atom:
        return redata.x**2+redata.y**2+redata.z**2
    return 1000

def make_distance(csv_adress1,csv_adress2,values=False):
    cluster1=pd.read_csv(csv_adress1,index_col=0)
    cluster2=pd.read_csv(csv_adress2,index_col=0)
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
        dis_=float()
        sumf=float()
        for val in f.values():
            sumf+=val.varValue
        for key,val in f.items():
            dis_+=val.varValue*costs[key]
        return dis_/sumf
    else:
        return nan