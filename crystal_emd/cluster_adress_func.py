import copy,os,glob,re
import pandas as pd
import subprocess
from collections import defaultdict
from .read_info import read_nood
import re
def fcluster_list(dir):
    if os.path.isfile('{}/picupadress'.format(dir)):
        cifdirs=pd.read_csv('{}/picupadress'.format(dir),index_col=0).cifadress.to_list()
    else:
        cifdirs= subprocess.getoutput("find {0} -type d | sort".format(dir))
        cifdirs= cifdirs.split('\n')
        del cifdirs[0]
    picinfo=list()
    cwd=os.getcwd()
    for _,cifdir in enumerate(cifdirs):
        cifid=re.split('/',cifdir)[-1]
        print(cifid)
        os.chdir(cifdir)
        try:
            csvn=glob.glob('*fcluster*')[0]
        except:
            print('no such file')
            os.chdir(cwd)
            continue
        info=pd.read_csv(csvn,index_col=0)
        picisite=copy.deepcopy(info.iloc[info.fclusternum.drop_duplicates().index].isite.values)
        picisite=[re.split("_", picisite_)[1] for picisite_ in picisite]
        picinfo_=[(cifid,cifdir,isite) for isite in picisite]
        picinfo+=picinfo_
        os.chdir(cwd)

    totalinfo=pd.DataFrame(picinfo,columns=['cifid','adress','isite'])
    totalinfo.to_csv('{}/allcif_cluster'.format(dir))
    return totalinfo

def isite_list(dir):
    #for i,adress in enumerate(csvlist):
    cifid=re.split('/',dir)[-1]
    ciflist=glob.glob('{}/{}_[0-9]*.csv'.format(dir,cifid))
    isitelist=[re.split('_',csvname)[-2] for csvname in ciflist]
    isitelist=list(set(isitelist))
    isitelist=[int(isitelist_) for isitelist_ in isitelist]
    isitelist.sort()
    picinfo=[(('{}').format(cifid),dir,isite) for isite in isitelist]
    resultdf=pd.DataFrame(picinfo,columns=['cifid','adress','isite'])
    resultdf.to_csv('{}/isite_list'.format(dir))
    return resultdf

def cluster_list(dir,dirs=False):
    #for i,adress in enumerate(csvlist):
    if dirs:
      clusterlist=glob.glob('{}/*/*_[0-9]*.csv'.format(dir))
    else:
      clusterlist=glob.glob('{}/*_[0-9]*.csv'.format(dir))
    result_=list()
    for i in clusterlist:
        filename=os.path.basename(i)
        dirname=os.path.dirname(i)
        cifid,isite,_=tuple(re.split('_',filename))
        result_.append((cifid,dirname,int(isite)))
    resultdf=pd.DataFrame(result_,columns=['cifid','adress','isite']).drop_duplicates()
    resultdf=resultdf.sort_values(by='cifid').reset_index(drop=True)
    return resultdf


def classification_ring_list(csvlist,outdir=None):
    if type(csvlist) is str:
        csvlist=pd.read_csv(csvlist,index_col=0)
    class_dict=defaultdict(list)
    
    for _,csv_ in csvlist.iterrows():
        csvname='{}/{}_{}_0.csv'.format(csv_.adress,csv_.cifid,csv_.isite)
        df=pd.read_csv(csvname,index_col=0).round(6)
        #counting duplicate isite
        disite=df.index.size-df.loc[:,'x':'z'].drop_duplicates().index.size
        #counting duplicate bond
        nooddf=pd.DataFrame(read_nood(df)).astype(str)
        dnood=nooddf.index.size-nooddf.drop_duplicates().index.size
        ring=disite-dnood
        class_dict[str(ring)].append((csv_.cifid,csv_.adress,csv_.isite))
    
    for key,adress in class_dict.items():
        if not type(outdir) is str:
            pd.DataFrame(adress,columns=['cifid','adress','isite']).to_csv('cluster_adress_ring={}'.format(key))
        else:
            pd.DataFrame(adress,columns=['cifid','adress','isite']).to_csv('{}/cluster_adress_ring={}'.format(outdir,key))


