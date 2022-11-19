from crystal_emd.show import emd_histgram,change
import sys
dirs='result/randzeo'
from glob import glob
import os,re
import matplotlib.pyplot as plt
ciflist=glob('result/randzeo/*/')
import pandas as pd
from crystal_emd.distance_func import cal_distance
from copy import deepcopy
def test_func(cifdir,database_adress='database',show=False,save=True,hist=False):
    distanlist=glob('{}/*distance'.format(cifdir))
    histdf=pd.DataFrame()
    for dataadress in distanlist:
        data=pd.read_csv(dataadress,index_col=0).iloc[0]
        if data.isite_i!='ID302_1':
            continue
        clusteradress_base='{}/{}_{}.csv'.format(database_adress,data.isite_j,data.pattern_j)
        clusteradress_cif='{}/{}_{}.csv'.format(cifdir,data.isite_i,data.pattern_i)
        change(clusteradress_base,clusteradress_cif,show=True)
        plt.close()
        df=change(clusteradress_base,clusteradress_cif,show=show,save=save,hist=hist)
        df.plot.barh(color='red')
        plt.yticks(rotation=30)
        plt.title('{}_to_{}'.format(data.isite_i,data.isite_j))
        plt.xlabel('angstrom')
        return df
for adress in ciflist:
    diradress=os.path.dirname(adress)
    cifid=re.split('/',adress)[-2]
    if cifid!='ID302':
        continue
    print(cifid)
    df=test_func(adress,hist=True)
    plt.show()
    plt.close()
    break