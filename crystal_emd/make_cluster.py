from .read_info import Set_Cluster_Info
import pickle,os,re
import pandas as pd
def make_cluster_dataset(cifid=None,atom='Si',nn_data_adress=None,nn_data=None,adjacent_num=None,isite=None,cluster_adress=None,clusterdf=None,rotation=True,outdir=None):
    cwd=os.getcwd()
    if not nn_data_adress is None:
        nn_data=pickle.load(open(nn_data_adress,'rb'))
        if cifid is None:
            cifid=re.sub('\.pickle','',os.path.basename(nn_data_adress))
    
    if not cluster_adress is None:
        clusterdf=pd.read_csv(cluster_adress,index_col=0)
        if cifid is None:
            cifid=re.sub('_[0-9]*_[0-9]*\.csv','',os.path.basename(cluster_adress))

    if cifid is None:
        print('please enter cifid')
    
    if not outdir is None:
        os.chdir(outdir)
    
    if not (isite is None and clusterdf is None):
        if not clusterdf is None:
            clusterinfo=Set_Cluster_Info(clusterdf=clusterdf)
            isite=clusterdf.iloc[0].isite
        else:
            clusterinfo=Set_Cluster_Info(isite,nn_data,adjacent_num)
        for pattern in range(len(clusterinfo.shaft_comb)):
            #print('\risite={} {}'.format(isite,pattern+1),end='')
            clusterinfo.parallel_shift_of_center()
            clusterinfo.rotation(pattern=pattern)
            clusterinfo.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
            if not rotation:
                break
    else:
        alllen_=0
        for isite in nn_data.keys():
            isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
            if isite_atom == 'Si':
                alllen_+=1
        cont=0
        for isite in nn_data.keys():
            isite_atom=re.split(r'([a-zA-Z]+)',nn_data[isite][0][0])[1]
            if isite_atom == 'Si':
                if adjacent_num is None:
                    print('please enter adjacent_num')
                    return
                clusterinfo=Set_Cluster_Info(isite,nn_data,adjacent_number=adjacent_num)
                alllen=alllen_*len(clusterinfo.shaft_comb)
                for pattern in range(len(clusterinfo.shaft_comb)):
                    #print("\r{}".format(pattern+1),end="")
                    clusterinfo.parallel_shift_of_center()
                    clusterinfo.rotation(pattern=pattern)
                    clusterinfo.cluster_coords.to_csv('{}_{}_{}.csv'.format(cifid,isite,pattern))
                    if not rotation:
                        break     
    os.chdir(cwd)
    return
