import copy,os,glob,re,subprocess
import pandas as pd

"""
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/sorttest'))
cifdir = cifdir_.split('\n')
del cifdir[0]
"""

dir='result/allzeorite'
cifdirs=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
cwd=os.getcwd()
picinfo=list()
for i,cifdir in enumerate(cifdirs):
    cifid=re.split('/',cifdir)[-1]
    print(cifid)
    os.chdir(cifdir)
    try:
        csvn=glob.glob('*fcluster*')[0]
    except:
        print('no such file')
        continue
    info=pd.read_csv(csvn,index_col=0)
    picisite=copy.deepcopy(info.iloc[info.fclusternum.drop_duplicates().index].isite.values)
    picinfo_=[(cifid,cifdir,isite) for isite in picisite]
    picinfo+=picinfo_
    os.chdir(cwd)

totalinfo=pd.DataFrame(picinfo,columns=['cifid','adress','isite'])
totalinfo.to_csv('{}/allcif_cluster'.format(dir))
