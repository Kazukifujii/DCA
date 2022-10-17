import numpy as np
import pandas as pd
import math

def make_degrres(csvfile):
    #df=pd.read_csv('./result/testcif/ABW/ABW_0_0.csv',index_col=0)
    df=pd.read_csv(csvfile,index_col=0)

    list1=[]

    for i in range(9):
        a=df.iat[i,3]
        b=df.iat[i,4]
        c=df.iat[i,5]
        x=np.array([a,b,c])

        list1.append(x)

    si1_0=list1[0]
    o1_1=list1[1]
    o1_2=list1[2]
    o1_3=list1[3]
    o1_4=list1[4]
    si1_1=list1[5]
    si1_2=list1[6]
    si1_3=list1[7]
    si1_4=list1[8]

    cos1=np.dot(o1_1,si1_1-o1_1)/(np.linalg.norm(o1_1)*np.linalg.norm(si1_1-o1_1))
    cos2=np.dot(o1_2,si1_2-o1_2)/(np.linalg.norm(o1_2)*np.linalg.norm(si1_2-o1_2))
    cos3=np.dot(o1_3,si1_3-o1_3)/(np.linalg.norm(o1_3)*np.linalg.norm(si1_3-o1_3))
    cos4=np.dot(o1_4,si1_4-o1_4)/(np.linalg.norm(o1_4)*np.linalg.norm(si1_4-o1_4))

    print(math.degrees(cos1),math.degrees(cos2),math.degrees(cos3),math.degrees(cos4))

#make_degrres('./result/testcif/ABW/ABW_0_0.csv')

