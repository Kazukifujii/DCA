from crystal_emd.show import emd_histgram

dirs='result/randzeo'
from glob import glob
import os,re
import matplotlib.pyplot as plt
ciflist=glob('result/randzeo/*/')
for adress in ciflist:
    diradress=os.path.dirname(adress)
    cifid=re.split('/',adress)[-2]
    if cifid!='ID302':
        continue
    print(cifid)
    df=emd_histgram(diradress,save=False)
    plt.close()
    df.iloc[0].sort_values().plot.barh(color='red')
    plt.yticks(rotation=30)
    plt.title('Maximum error for each cluster in {}'.format(cifid))
    plt.xlabel('angstrom')
    plt.show()
    #plt.savefig('Maximum_error_for_each_cluster_in_{}.svg'.format(cifid))
    break