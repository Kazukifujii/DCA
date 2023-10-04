import os
import re
import pickle
import shutil
from collections import defaultdict
import numpy as np
import subprocess
import glob
from pymatgen.core.structure import IStructure
from pymatgen.io.vasp.inputs import Poscar

def read_nnlist(nnlist_path:str,siteinfo:dict,max_neib:dict) -> dict():
    """
    Make nnlist.
    """
    nnfile = open(nnlist_path).readlines()
    nnlist = defaultdict(list)
    for i in nnfile:
        info = re.split('\s+',i)[1:-1]
        center_isite = int(info[0])
        neighbor_isite = int(info[1])
        distance = float(info[2])
        coord = [float(info[3]),float(info[4]),float(info[5])]
        neighbor_isite_info = [int(info[6]),int(info[7]),int(info[8])]
        #add nnlist
        nnlist[center_isite].append((neighbor_isite,distance,coord,neighbor_isite_info))
    nnlist = dict(nnlist)
    #sort 
    for isite,atom in siteinfo.items():
        nnlist[isite].sort(key=lambda x:x[1])
        nnlist[isite]=nnlist[isite][1:max_neib[atom]+1]
    return nnlist

def nnlist2nn_data(nnlist:dict,siteinfo:dict) -> dict():
    #set nn_data
    nn_data=defaultdict(list)
    #center_info=[siteinfo[1],np.nan,0,0,0]
    for isite,neibs in nnlist.items():
        center_info = [siteinfo[isite],np.nan,0,0,0]
        nn_data[isite].append(center_info)
        for neib_isite,_,coord,_ in neibs:
            nn_data_=[neib_isite,siteinfo[neib_isite],*coord]
            nn_data[isite].append(nn_data_)
    return dict(nn_data)

def read_siteinfo_from_poscar(filepath:str) -> dict():
    """
    Read siteinfo from a POSCAR file.
    """
    poscar = open(filepath).readlines()
    #directを含む行のインデックスを取得
    direct_line = poscar.index('direct\n')
    isite_info = {i+1:coords.split(' ')[-1].replace('\n','') for i,coords in enumerate(poscar[direct_line+1:])}
    return isite_info

def run_make_nnlist_out(fileaddress='POSCAR', rmax=1.0):
    """
    Generate nnlist using an external program.
    """
    subprocess.run(f'make_nnlist.out {fileaddress} {rmax} >> {fileaddress}.log', shell=True)

def make_poscar(ciffile):
    """
    Generate a POSCAR file from a CIF file.
    """
    filename = os.path.basename(ciffile)
    poscar = Poscar(IStructure.from_file(ciffile))
    outposcar = '{}_poscar'.format(filename)
    poscar.write_file(outposcar)

def make_nn_data_from_cifdirs(dirpath:str, outputpath:str,max_neib:dict={'Si':4,'O':2}):
    """
    Generate nn_data.pickle from CIF directories.
    """
    cwd = os.getcwd()
    result_dir_path = os.path.join(outputpath,dirpath)
    
    #make output directory
    if not os.path.isdir(outputpath):
        os.makedirs(result_dir_path)
    else:
        if not os.path.isdir(result_dir_path):
            os.makedirs(result_dir_path)
    ciffilelist = glob.glob(os.path.join(dirpath, '*.cif'))

    for cif_path in ciffilelist:
        basename = os.path.basename(cif_path)
        cifnum = basename.replace('.cif', '')
        result_path = 'nb_{}.pickle'.format(cifnum)

        cifdataout = os.path.join(result_dir_path,cifnum)
        if not os.path.isdir(cifdataout):
            os.mkdir(cifdataout)
        shutil.copyfile(cif_path, os.path.join(cifdataout, basename))

        os.chdir(cifdataout)
        try:
            make_poscar(basename)
            run_make_nnlist_out('{}_poscar'.format(basename),5)
            siteinfo = read_siteinfo_from_poscar('{}_poscar'.format(basename))
            nnlist = read_nnlist('{}_poscar.nnlist'.format(basename), siteinfo, max_neib)
            nn_data = nnlist2nn_data(nnlist, siteinfo)

            #save nn_data
            if os.path.isfile(result_path):
                os.remove(result_path)
            with open(result_path,'wb') as f:
                pickle.dump(nn_data,f)
        except:
            pass
        os.chdir(cwd)