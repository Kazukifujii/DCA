import os,re,pickle
from collections import defaultdict
from numpy import nan

def make_nn_data_from_nnlist(fileadress,siteinfo):
    #make nn_data.pickle from file of nnlis
    #set init info
    f=open(fileadress,'r').readlines()
    filename=re.split('/',fileadress)[-1]
    resultfile='{}.pickle'.format(filename.replace('.nnlist',''))
    resultadress=fileadress.replace(filename,'')
    resultadress='{}{}'.format(resultadress,resultfile)
    nnlist=defaultdict(list)
    #read nnlist
    for i in f:
        float_info=re.findall('\-*\d+\.?\d+',i)
        int_info=re.findall('\-*\d+',i)
        int_info=[int(int_info_) for int_info_ in int_info]
        float_info=[float(float_info_) for float_info_ in float_info]
        nnlist[int_info[0]].append((int_info[1],float_info[0],float_info[1::],int_info[-3::]))
    #sort
    for i in nnlist.keys():
        nnlist[i].sort(key=lambda x:x[1])
        nnlist[i]=nnlist[i][1:5]
    #set nn_data
    nn_data=defaultdict(list)
    center_info=[siteinfo[0],nan,0,0,0]
    for i in nnlist.keys():
        nn_data[i].append(center_info)
        for isite,distace,coord,cell in nnlist[i]:
            nn_data_=[isite,siteinfo[isite-1],*coord]
            nn_data[i].append(nn_data_)
    if os.path.isfile(resultadress):
        os.remove(resultadress)
    with open(resultadress,'wb') as f:
        pickle.dump(nn_data,f)
    return

def read_sitinfo_poscar(filename):
    siteinfo=list()
    for i in reversed(open(filename,'r').readlines()):
        splitinfo=re.findall('\w+',i)
        if len(splitinfo)==1:
            break
        siteinfo.append(splitinfo[-1])
    return siteinfo

def isolation_poscars(fileadress='init_POSCARS'):
    filename=os.path.basename(fileadress)
    dirname=os.path.dirname(fileadress)
    d=open(fileadress,'r').readlines()
    idlist=list()
    for I,i in enumerate(d):
        if re.match('ID',i):
            idlist.append(I)
    cwd=os.getcwd()
    os.chdir(dirname)
    for I,i in enumerate(idlist):
        idname=d[idlist[I]].replace('\n','')
        if int(len(idlist)-1)==I:
            poscar=d[idlist[I]::]
            f=open('{}_POSCAR'.format(idname),'w')
            f.writelines(poscar)
            f.close()
            continue
        poscar=d[idlist[I]:idlist[I+1]]
        f=open('{}_POSCAR'.format(idname),'w')
        f.writelines(poscar)
        f.close()
    os.chdir(cwd)

import subprocess 
def make_nnlist(fileadress='POSCAR',rmax=1.0):
    
    """cwd=os.getcwd()
    dirname=os.path.dirname(fileadress)
    filename=os.path.basename(fileadress)
    os.chdir(dirname)
    print(dirname)"""
    subprocess.run('a.out {} {}'.format(fileadress,rmax),shell=True)
    #s.chdir(cwd)
    return