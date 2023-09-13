from subprocess import run
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
import argparse,os
import pickle
import glob
import json
import pandas as pd
from joblib import Parallel, delayed
from Distance_based_on_Cluster_Analysis.characterization import CrystalFeatureCalculator
def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--config-path',default='config',help='config path')
    return pares.parse_args()



def parallen_make_cluster_dataset(data,adjacent_num=2):
      nn_data_address= os.path.join(data.cifaddress,f"nb_{data.cifid}.pickle")
      make_cluster_dataset(cifid=data.cifid,nn_data_address=nn_data_address,adjacent_num=adjacent_num,rotation=False,outdir=data.cifaddress)
      return 
  

def parallel_calculate_feature(data,characteriz_func):
    #特徴量を計算し、各ディレクトリに結果を保存
    feature = characteriz_func.calculate_features(data.cifaddress)

    #特徴量の保存
    resulttxt=f'{data.cifaddress}/cifpoint'
    cifid=os.path.basename(data.cifaddress)
    text_file=open(resulttxt,'w')
    text_file.write('cifid,point\n')
    text_file.write('{},{}\n'.format(cifid,feature))
    text_file.close()
    #logの保存
    #ディレクトリの作成
    os.makedirs(f'{data.cifaddress}/log',exist_ok=True)

    for j,log in enumerate(characteriz_func.calculate_log):
      pickle.dump(log,open(f'{data.cifaddress}/log/{cifid}_{j}.pickle','wb'))
    return 

def load_params_from_config(config:configparser.ConfigParser):
  float_keys = ['reference','sep_value']
  ing_keys = ['offset','eig_max_neiber_num']
  bool_keys = ['use_mesh_flag']
  list_keys = ['target_atoms']
  params = dict(config['CALCULATION'])
  n_jobs = int(params.pop('n_jobs'))
  adjacent_num = int(params.pop('adjacent_num'))
  for key in float_keys:
        params[key] = float(params[key])

  for key in ing_keys:
      params[key] = int(params[key])

  for key in bool_keys:
      params[key] = bool(params[key])

  for key in list_keys:
      params[key] = json.loads(params[key].replace("'", "\""))
  
  return params,n_jobs,adjacent_num
   
import contextlib
from typing import Optional
import joblib
from tqdm.auto import tqdm

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


import configparser
def main():
  config = configparser.ConfigParser()
  config.read('config')
  database_path = config['PATH LIST']['database-path']
  cifdir = config['PATH LIST']['cifdir']

  params,n_jobs,adjacent_num = load_params_from_config(config)
  
  params.update({'databasepath':database_path})

  resultdir=os.path.join('result',cifdir)
  #cifから隣接情報の取出し
  run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
  print('emd make_adjacent_tabel')
  run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
  print('ok')

  #隣接情報からクラスターを生成
  print('make cluster dataset')
  picdata=make_sort_ciffile(resultdir,estimecont='all')
  with tqdm_joblib(len(picdata)):
    Parallel(n_jobs=n_jobs)([delayed(parallen_make_cluster_dataset)(data,adjacent_num) for _,data in picdata.iterrows()])
  print('ok')
  #各cifファイルの特徴量を計算
  print('load database')
  characteriz_func=CrystalFeatureCalculator(**params)
  print('ok')

  #特徴量の計算
  with tqdm_joblib(len(picdata)):
    Parallel(n_jobs=n_jobs)([delayed(parallel_calculate_feature)(data,characteriz_func) for _,data in picdata.iterrows()])

  #各cifファイルの特徴量を結合

  point_files = glob.glob(f'{resultdir}/*/cifpoint')
  point_df = [pd.read_csv(file_i) for file_i in point_files]
  point_df = pd.concat(point_df)
  point_df.to_csv(f'{resultdir}/cifpoint',index=False)

if __name__=='__main__':
  main()