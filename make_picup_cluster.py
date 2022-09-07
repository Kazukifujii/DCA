import copy,os,glob,re,subprocess
import pandas as pd


cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/sorttest'))
cifdir = cifdir_.split('\n')
del cifdir[0]
cwd=os.getcwd()
for i in cifdir:
    cifid=re.split('/',i)[-1]
    if cifid!='AEI':
        continue
    print(cifid)
    os.chdir(i)
    csvn=glob.glob('*fcluster*')[0]
    info=pd.read_csv(csvn,index_col=0)
    print(info.head(5))
    os.chdir(cwd)
