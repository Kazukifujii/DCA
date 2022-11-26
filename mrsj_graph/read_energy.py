#pcodのデータを整理
from glob import glob
'''
ciflist=glob('../*cif')
import re,os
import pandas as pd
energy_list=list()
for i,cifname in enumerate(ciflist):
    cifid=os.path.basename(cifname).replace('.cif','')
    #print(cifid)
    print('\r{}/{}'.format(i+1,len(ciflist)),end='')
    for text_i in open(cifname).readlines():
        if re.search('GULP energy per Si atom',text_i):
            float_txt=re.findall('\-*\d+\.?\d+',text_i)
            if len(float_txt)!=1:
                print('not energy len',cifid)
            float_info=float(float_txt[0])
            energy_list.append((cifid,float_info))
print()
df=pd.DataFrame(energy_list,columns=['cifid','GULP energy per Si atom'])
df.to_csv('GULP_energy_per_Si_atom.csv')
'''
import pandas as pd

energydf=pd.read_csv('GULP_energy_per_Si_atom.csv',index_col=0)
pointfile='cifpoint_average'
pointdf=pd.read_csv(pointfile)

pointdf=pointdf.dropna()
pointdf=pd.merge(pointdf,energydf)
import matplotlib.pyplot as plt
plt.scatter(pointdf.iloc[:,1],pointdf.iloc[:,2])
plt.xlabel('{}  (angstrom)'.format('distance base cluster anarysis'))
plt.ylabel('{}  (kJ/mol)'.format(pointdf.iloc[:,1:3].columns.to_list()[1]))
plt.title(pointfile)
plt.show()