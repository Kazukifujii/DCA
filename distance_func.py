from cmath import nan
import pandas as pd
import pulp

def calcost(data1,data2):
    redata=data1-data2
    return (redata.x**2+redata.y**2+redata.z**2)**2

def make_distance(csv_adress1,csv_adress2):
    cluster1=pd.read_csv(csv_adress1,index_col=0)
    cluster2=pd.read_csv(csv_adress2,index_col=0)
    #make cost and constrains
    costs=dict()
    for i,data1 in cluster1.loc[:,'x':'z'].iterrows():
        for j,data2 in cluster2.loc[:,'x':'z'].iterrows():
            costs[(i,j)]=calcost(data1,data2)

    model=pulp.LpProblem('cluster_matching',pulp.LpMinimize)
    x=dict()
    obfunc=list()
    for index,cost in costs.items():
        i,j=index
        x[i,j]=pulp.LpVariable('index{}_{}'.format(i,j),lowBound=0)
        obfunc.append(x[i,j]*cost)
    model+=pulp.lpSum(obfunc)

    sum1_=cluster1.loc[:,'x':'z']**2
    colsum1=sum1_.sum(axis=1)
    for i,data1 in cluster1.iterrows():
        model += pulp.lpSum([x[(i,j)] for j,_ in cluster2.iterrows()])==colsum1[i]

    sum2_=cluster1.loc[:,'x':'z']**2
    colsum2=sum2_.sum(axis=1)
    for j,data2 in cluster2.iterrows():
        model+= pulp.lpSum([x[(i,j)] for i,_ in cluster1.iterrows()])==colsum2[j]

    result=model.solve(pulp.PULP_CBC_CMD(msg = False))
    if result==1:
        dis_=float()
        sumf=float()
        for val in x.values():
            sumf+=val.varValue
        for key,val in x.items():
            dis_+=val.varValue*costs[key]
        return dis_/sumf
    else:
        return nan