from subprocess import run
from copy import deepcopy
import shutil,os,re,pickle
from math import nan
import numpy as np
from collections import defaultdict

def make_randzeo(file_num,outdir=None):
    if not outdir is None:
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        os.mkdir(outdir)
        for i in range(file_num):
            run('randzeo.out 5.0  7.0 8.0  2.8 3.2  6 >> {}/ID{}.randzeo'.format(outdir,i),shell=True)
        return
    for i in range(file_num):
            run('randzeo.out 5.0  7.0 8.0  2.8 3.2  6 >> ID{}.randzeo'.format(i),shell=True)
    return

def make_nn_data_from_randzeo(filename):
    bn=os.path.basename(filename)
    di=os.path.dirname(filename)
    if len(di)!=0:
        resultaddress='{}/{}.pickle'.format(di,bn)
    else:
        resultaddress='{}.pickle'.format(bn)
    f=open(filename,'r').readlines()
    nn_data=defaultdict(list)
    site_coords=dict()
    for txt in f:
        if re.search('rmin rmax=',txt):
            lattice_c=list(map(float,re.findall('\-*\d+\.?\d+',txt)[0:3]))
            a,b,c=tuple(map(float,re.findall('\-*\d+\.?\d+',txt)[0:3]))
        if re.search('!pos cartsian',txt):
            float_info=list(map(float,re.findall('\-*\d+\.?\d+',txt)))
            isite=int(re.findall('\d+',txt)[-1])
            center_info=['Si1',nan,*float_info]
            site_coords[isite]=deepcopy(np.array(float_info))
            nn_data[isite].append(center_info)
        if re.search('!pair index',txt):
            isite_i,isite_j=tuple(map(int,re.findall('\d+',txt)))
            site_coord_i=site_coords[isite_i]
            dfsite_coord_j=site_coords[isite_j]-site_coord_i
            mdi=1000
            for i in [0,1,-1]:
                for j in [0,1,-1]:
                    for k in [0,1,-1]:
                        r=np.array([a*i,b*j,c*k])
                        recoord_=r+dfsite_coord_j
                        di=np.linalg.norm(recoord_)
                        if mdi>=di:
                            mdi=deepcopy(di)
                            recoord=deepcopy(recoord_+site_coord_i)
            nn_data[isite_i].append([isite_j,'Si1',*recoord])
    with open(resultaddress,'wb') as bd:
        pickle.dump(nn_data,bd)
    return nn_data
