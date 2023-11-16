from subprocess import run
import os,subprocess,shutil
from Distance_based_on_Cluster_Analysis.distance import CalulateSelfDistance
from Distance_based_on_Cluster_Analysis.clustering import make_clustering,fcluster_list
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
from Distance_based_on_Cluster_Analysis.clustermanager import ClusterManager
import argparse
import logging
from tqdm import tqdm
from joblib import Parallel, delayed
import json
import contextlib
from typing import Optional
import joblib
from tqdm.auto import tqdm
from functools import partial


@contextlib.contextmanager
def tqdm_joblib(total: Optional[int] = None, **kwargs):
    #https://blog.ysk.im/x/joblib-with-progress-bar
    pbar = tqdm(total=total, miniters=1, smoothing=0, **kwargs)

    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            pbar.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback

    try:
        yield pbar
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        pbar.close()


def parallel_clustering_in_crystal(cifid,result_base_path,csd:CalulateSelfDistance,logger=None):
    outdir = os.path.join(result_base_path,cifid)
    #距離の計算
    try:
        cluster_distance_df=csd.calculate_distance(outdir)
    except :
        logger.exception('cal_distance error:cifid {}'.format(cifid))
        return
    cluster_distance_df.to_csv(os.path.join(outdir,f"{cifid}_cluster_distance.csv"))
    #クラスタリングによる分類
    flusterdf=make_clustering(cluster_distance_df)
    #結果の保存
    flusterdf.to_csv(os.path.join(outdir,f"{cifid}_fcluster.csv"))

    
def parallel_make_cluster(data):
    clusteraddress = os.path.join(data.address,f'{data.cifid}_{data.isite}_0.csv')
    make_cluster_dataset(cluster_address=clusteraddress,outdir=data.address)

import configparser
def parse_config(path='config.ini'):
    config = configparser.ConfigParser()
    config.read(path)

    args = {
        'cifdir': config.get('DEFAULT', 'cifdir', fallback='cifdirs/allzeolite'),
        'adjacent_num': config.getint('DEFAULT', 'adjacent_num', fallback=2),
        'cluster_atom_num': json.loads(config.get('DEFAULT', 'cluster_atom_num', fallback='{"Si":5,"O":4}')),
        'max_neib': json.loads(config.get('DEFAULT', 'max_neib', fallback='{"Si":4,"O":2}')),
        'adjacency_algorithm': config.get('DEFAULT', 'adjacency_algorithm', fallback='neib'),
        'outdirname': config.get('DEFAULT', 'outdirname', fallback='cluster_database')
    }

    return args

def main():
    args = parse_config('config/makedataset_config.ini')
    cifdir=args['cifdir']
    adjacent_num=args['adjacent_num']
    cluster_atom_num=args['cluster_atom_num']
    max_neib = args['max_neib']
    adjacency_algorithm = args['adjacency_algorithm']
    database=args['outdirname']

    result_base_path = f'result/{cifdir}'
    
    #既存のディレクトリがある場合は削除
    if os.path.isdir(result_base_path):
        shutil.rmtree(result_base_path)

    #cifから隣接情報の取出し
    if adjacency_algorithm=='neib':
        from Distance_based_on_Cluster_Analysis.make_nn_data_from_fortran import CIFDataProcessor
        maker = CIFDataProcessor(max_neib=max_neib,algorithm='pymatgen')
        maker.make_nn_data_from_cifdirs(cifdir,result_base_path)
    elif adjacency_algorithm=='chemenv':
        
        run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
        run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
    import glob
    cifid_list = glob.glob(os.path.join(cifdir,'*.cif'))
    cifid_list = [os.path.basename(i).replace('.cif','') for i in cifid_list]

    #隣接情報からクラスターを生成
    #picdata=make_sort_ciffile(f'result/{cifdir}',estimecont='all')
    cwd = os.getcwd()
    print('make cluster dataset')
    allciflen=len(cifid_list)
    for i,cifid in enumerate(cifid_list):
        print(f'\r{cifid} {i+1}/{allciflen}',end='')
        nn_data_address= os.path.join(result_base_path,cifid,f'nb_{cifid}.pickle')
        outdir = os.path.join(result_base_path,cifid)
        make_cluster_dataset(cifid=cifid,adjacent_num=adjacent_num,nn_data_address=nn_data_address,outdir=outdir,rotation=False)
    print('')
    print('ok')

    #異常なクラスターを削除
    #異常なクラスターを別ディレクトリに保存
    #保存先のディレクトリを作成
    print('clean up cluster')
    error_dir_path = f'result/{cifdir}/error_clusters'
    logfile_path = f'result/{cifdir}/clean up_cluster.log'

    if os.path.isdir(error_dir_path):
        shutil.rmtree(error_dir_path)        
    os.mkdir(error_dir_path)
    if os.path.isfile(logfile_path):
        os.remove(logfile_path)
    
    cm = ClusterManager.from_dirpath(result_base_path,dirs=True,ignore_dirs=[error_dir_path])
    cm.to_file_path()
    for i in range(len(cm.cluster_path_list_df)):
        clusteraddress = cm.cluster_path_list_df.iloc[i,0]
        if not os.path.isfile(clusteraddress):
            print('no file',clusteraddress)
            continue
        clustertext = open(clusteraddress,'r').readlines()
        count = [sum([i.count(j) for i in clustertext]) for j in cluster_atom_num.keys()]
        if count != list(cluster_atom_num.values()):
            f=open(logfile_path,'a')
            f.write(f'{clusteraddress}\n')
            f.close()
            shutil.move(clusteraddress,error_dir_path)
    print('ok')
    del cm
    
    #残っているクラスターの回転パターンを全て取る
    print('make all pattern')
    cm = ClusterManager.from_dirpath(f'result/{cifdir}',dirs=True,ignore_dirs=[error_dir_path])
    with tqdm_joblib(total=len(cm.cluster_list_df)):
        Parallel(n_jobs=-1)(delayed(parallel_make_cluster)(data) for _,data in cm.cluster_list_df.iterrows())
    del cm
    print('ok')
    
    # ログの出力名を設定
    logger = logging.getLogger('DistanceLogg')
    fh = logging.FileHandler('cal_distance_error.log')
    logger.addHandler(fh)
    #各結晶に属するクラスターの距離を計算(等価なクラスター  を取り出すため)
    
    #set logger and CalulateSelfDistance
    csd=CalulateSelfDistance(target_atoms=list(cluster_atom_num.keys()),reference=1e-8,chunk=30000)
    parallel_clustering = partial(parallel_clustering_in_crystal,csd=csd,logger=logger)
    print('cal self distance')
    with tqdm_joblib(total=len(cifid_list)):
        Parallel(n_jobs=-1)(delayed(parallel_clustering)(cifid,result_base_path) for cifid     in cifid_list)
    print('ok')

    fcluster_df=fcluster_list(cifid_list,result_base_path)
    fcluster_df.to_csv(f'result/{cifdir}/unique_cluster.csv')

    print('make database')
    if os.path.isdir(database):
        shutil.rmtree(database)
    os.mkdir(database)

    for i,data in fcluster_df.iterrows():
        for pattern in range(12):
            clusteraddress=f'{data.address}/{data.cifid}_{data.isite}_{pattern}.csv'
            if not os.path.isfile(clusteraddress):
                print('not file ',clusteraddress)
            copyaddress=f'{database}/{data.cifid}_{data.isite}_{pattern}.csv'
            shutil.copy(clusteraddress,copyaddress)
    print('ok')
if __name__=='__main__':
    main()
