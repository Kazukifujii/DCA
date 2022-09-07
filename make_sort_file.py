import subprocess
import re

cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('/home/fujikazuki/crystal_emd/result/allzeorite'))
cifdir = cifdir_.split('\n')
del cifdir[0]
isiteinfo=list()
for i in cifdir:
    cifid=re.split('/',i)[-1]
    lasttxt=subprocess.getoutput("grep ' Si' {}/{}.txt |tail -n 1".format(i,cifid))
    maxisite=int(re.split('Si',lasttxt)[0].replace(' ',''))
    isiteinfo.append((cifid,maxisite))
isiteinfo.sort(key=lambda x:x[1])
for i in isiteinfo:
    print(i)
