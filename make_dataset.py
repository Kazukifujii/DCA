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


def parallel_clustering_in_crystal(data,csd:CalulateSelfDistance,logger=None):
    cifid=data.cifid
    #距離の計算
    try:
        cluster_distance_df=csd.calculate_distance(data.cifaddress)
    except :
        logger.exception('cal_distance error:cifid {}'.format(cifid))
        return
    cluster_distance_df.to_csv(f"{data.cifaddress}/{cifid}_cluster_distance.csv")
    #クラスタリングによる分類
    flusterdf=make_clustering(cluster_distance_df)
    #結果の保存
    flusterdf.to_csv(f"{data.cifaddress}/{cifid}_fcluster.csv")


def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--cifdir',default='cifdirs/allzeolite',help='zeolitecif')
    pares.add_argument('--adjacent_num',default=2,help='(int)')
    pares.add_argument('--cluster_atom_num',default='{"Si1":5,"O1":4}',help='(json)')
    pares.add_argument('--outdirname',default='cluster_database')
    return pares.parse_args()

def main():
    pares=pares_args()
    cifdir=pares.cifdir
    adjacent_num=int(pares.adjacent_num)
    cluster_atom_num=json.loads(pares.cluster_atom_num)
    database=pares.outdirname
    
    #cifから隣接情報の取出し
    run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
    run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
    
    #隣接情報からクラスターを生成
    picdata=make_sort_ciffile(f'result/{cifdir}',estimecont='all')
    cwd = os.getcwd()
    
    allciflen=picdata.shape[0]
    for i,data in picdata.iterrows():
        print(f'\r{data.cifid} {i+1}/{allciflen}',end='')
        nn_data_address= subprocess.getoutput(f"find {data.cifaddress} -name nb_*.pickle")
        make_cluster_dataset(cifid=data.cifid,adjacent_num=adjacent_num,nn_data_address=nn_data_address,outdir=data.cifaddress,rotation=False)
    print('')

    #異常なクラスターを削除
    cm = ClusterManager.from_dirpath(f'result/{cifdir}',dirs=True)
    cm.to_file_path()
    for i in range(len(cm.cluster_path_list_df)):
        clusteraddress = cm.cluster_path_list_df.iloc[i,0]
        if not os.path.isfile(clusteraddress):
            print('no file',clusteraddress)
            continue
        clustertext = open(clusteraddress,'r').readlines()
        count = [sum([i.count(j) for i in clustertext]) for j in cluster_atom_num.keys()]
        if count != list(cluster_atom_num.values()):
            f=open('clean up_cluster.log','a')
            f.write(f'{clusteraddress}\n')
            os.remove(clusteraddress)
            f.close()
    
    del cm
    
    #残っているクラスターの回転パターンを全て取る
    print('make all pattern')
    cm = ClusterManager.from_dirpath(f'result/{cifdir}',dirs=True)
    cm.to_file_path()
    allciflen = cm.cluster_list_df.shape[0]
    for i in  range(len(cm.cluster_list_df)):
        data = cm.cluster_list_df.iloc[i,:]
        print(f'\r{data.cifid} {i+1}/{allciflen}',end='')
        clusteraddress = cm.cluster_path_list_df.iloc[i,0]
        make_cluster_dataset(cluster_address=clusteraddress,outdir=data.address)
    
    del cm
    
    # ログの出力名を設定
    logger = logging.getLogger('DistanceLogg')
    fh = logging.FileHandler('cal_distance_error.log')
    logger.addHandler(fh)
    #各結晶に属するクラスターの距離を計算(等価なクラスターを取り出すため)
    
    #set logger and CalulateSelfDistance
    csd=CalulateSelfDistance(target_atoms=['Si1','O1'],reference=1e-8,chunk=30000)
    parallel_clustering = partial(parallel_clustering_in_crystal,csd=csd,logger=logger)

    with tqdm_joblib(total=len(picdata)):
        Parallel(n_jobs=-1)(delayed(parallel_clustering)(data) for _,data in picdata.iterrows())
    
    fcluster_df=fcluster_list(picdata)
    fcluster_df.to_csv(f'result/{cifdir}/unique_cluster.csv')
    
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

if __name__=='__main__':
    main()
