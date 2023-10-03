'''import re,pickle
from collections import defaultdict
from numpy import nan
import shutil
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

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.core.structure import IStructure
import os
def make_poscar(ciffile):
    filename=os.path.basename(ciffile)
    poscar=Poscar(IStructure.from_file('{}'.format(ciffile)))
    outposcar='{}_poscar'.format(filename)
    poscar.write_file(outposcar)

from tqdm import tqdm
def make_nn_data_from_cifdirs(dirpath,outputpath,restart=False):
    cwd = os.getcwd()
    result_path = os.path.join(outputpath,dirpath)
    if not os.path.isdir(outputpath):
        os.makedirs(result_path)
    else:
        if not os.path.isdir(result_path):
            os.makedirs(result_path)
    import glob
    ciffilelist = glob.glob(os.path.join(dirpath ,'*.cif'))
    #print(ciffilelist)

    checker = restart
    print('make adjacent info by pymatgen')
    for cif_path in tqdm(ciffilelist):
        #cifnum = re.findall('\/(\w+)\.cif',i)[0]
        basename=os.path.basename(cif_path)
        cifnum=basename.replace('.cif','')
        if cifnum == restart or not checker:
            checker = True

        if checker:
            cifdataout = os.path.join(outputpath,dirpath,cifnum)
            if not os.path.isdir(cifdataout):
                os.mkdir(cifdataout)
            
            shutil.copyfile(cif_path,os.path.join(cifdataout,basename))
            os.chdir(cifdataout)
            make_poscar(basename)
            make_nnlist('{}_poscar'.format(basename))
            siteinfo=read_sitinfo_poscar('{}_poscar'.format(basename))
            make_nn_data_from_nnlist('{}.nnlist'.format(basename),siteinfo)
            os.chdir(cwd)

    print('end adjacent info')

'''
import os
import re
import pickle
import shutil
from collections import defaultdict
from numpy import nan
import subprocess
from tqdm import tqdm
import glob
from pymatgen.core.structure import IStructure
from pymatgen.io.vasp.inputs import Poscar
"""
def make_nn_data_from_nnlist(fileaddress, siteinfo):
    '''
    Make nn_data.pickle from a file of nnlist.
    '''
    filename = os.path.split(fileaddress)[-1]
    resultfile = '{}.pickle'.format(filename.replace('.nnlist', ''))
    resultaddress = os.path.join(os.path.dirname(fileaddress), resultfile)
    nnlist = defaultdict(list)

    with open(fileaddress, 'r') as f:
        for line in f:
            float_info = re.findall(r'-?\d+\.?\d+', line)
            int_info = re.findall(r'-?\d+', line)
            int_info = [int(int_info_) for int_info_ in int_info]
            float_info = [float(float_info_) for float_info_ in float_info]
            nnlist[int_info[0]].append((int_info[1], float_info[0], float_info[1:], int_info[-3:]))

    for key in nnlist.keys():
        nnlist[key].sort(key=lambda x: x[1])
        nnlist[key] = nnlist[key][1:5]

    nn_data = defaultdict(list)
    center_info = [siteinfo[0], nan, 0, 0, 0]
    for key in nnlist.keys():
        nn_data[key].append(center_info)
        for isite, distance, coord, cell in nnlist[key]:
            nn_data_ = [isite, siteinfo[isite - 1], *coord]
            nn_data[key].append(nn_data_)

    if os.path.isfile(resultaddress):
        os.remove(resultaddress)
    with open(resultaddress, 'wb') as f:
        pickle.dump(nn_data, f)
"""
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


def read_siteinfo_poscar(filepath):
    """
    Read siteinfo from a POSCAR file.
    """
    poscar = open(filepath).readlines()
    for i,text in enumerate(poscar):
        if ('direct' in text):
            break
        isite_info = {i+1:re.findall(r'\w+',coords)[-1] for i,coords in enumerate(poscar[8:])}
    return isite_info

def make_nnlist(fileaddress='POSCAR', rmax=1.0):
    """
    Generate nnlist using an external program.
    """
    subprocess.run(f'a.out {fileaddress} {rmax}', shell=True)

def make_poscar(ciffile):
    """
    Generate a POSCAR file from a CIF file.
    """
    filename = os.path.basename(ciffile)
    poscar = Poscar(IStructure.from_file(ciffile))
    outposcar = '{}_poscar'.format(filename)
    poscar.write_file(outposcar)

def make_nn_data_from_cifdirs(dirpath, outputpath, restart=False):
    """
    Generate nn_data.pickle from CIF directories.
    """
    cwd = os.getcwd()
    result_path = os.path.join(outputpath,dirpath)
    
    if not os.path.isdir(outputpath):
        os.makedirs(result_path)
    else:
        if not os.path.isdir(result_path):
            os.makedirs(result_path)

    ciffilelist = glob.glob(os.path.join(dirpath, '*.cif'))
    checker = restart
    print('make adjacent info by pymatgen')
    for cif_path in ciffilelist:
        basename = os.path.basename(cif_path)
        cifnum = basename.replace('.cif', '')
        if cifnum == restart or not checker:
            checker = True
        
        if checker:
            cifdataout = os.path.join(result_path,cifnum)
            if not os.path.isdir(cifdataout):
                os.mkdir(cifdataout)
            shutil.copyfile(cif_path, os.path.join(cifdataout, basename))
            os.chdir(cifdataout)
            make_poscar(basename)
            make_nnlist('{}_poscar'.format(basename),5)
            siteinfo = read_siteinfo_poscar('{}_poscar'.format(basename))
            make_nn_data_from_nnlist('{}_poscar.nnlist'.format(basename), siteinfo)
            os.chdir(cwd)

    print('end adjacent info')