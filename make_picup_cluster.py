import copy,os,glob,re
import pandas as pd
import subprocess

def make_picup_cluster(dir):
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
        if cifid=='GIS':
            break
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
