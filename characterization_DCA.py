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
import configparser

def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--config-path',default='config',help='config path')
    return pares.parse_args()



def parallen_make_cluster_dataset(data,adjacent_num=2):
      nn_data_address= os.path.join(data.cifaddress,f"nb_{data.cifid}.pickle")
      make_cluster_dataset(cifid=data.cifid,nn_data_address=nn_data_address,adjacent_num=adjacent_num,rotation=False,outdir=data.cifaddress)
      return 
  

def parallel_calculate_feature(path,characteriz_func):
    #特徴量を計算し、各ディレクトリに結果を保存
    feature = characteriz_func.calculate_features(path)

    #特徴量の保存
    resulttxt=f'{path}/cifpoint'
    cifid=os.path.basename(path)
    text_file=open(resulttxt,'w')
    text_file.write('cifid,point\n')
    text_file.write('{},{}\n'.format(cifid,feature))
    text_file.close()
    #logの保存
    #ディレクトリの作成
    os.makedirs(f'{path}/log',exist_ok=True)

    for j,log in enumerate(characteriz_func.calculate_log):
      pickle.dump(log,open(f'{path}/log/{cifid}_{j}.pickle','wb'))
    return 

def load_params_from_config(config:configparser.ConfigParser):
  float_keys = ['reference','sep_value']
  ing_keys = ['offset']
  bool_keys = ['use_mesh_flag']
  list_keys = ['target_atoms','max_neib']
  params = dict(config['CALCULATION'])
  n_jobs = int(params.pop('n_jobs'))
  adjacent_num = int(params.pop('adjacent_num'))
  for key in float_keys:
        params[key] = float(params[key])

  for key in ing_keys:
      params[key] = int(params[key])

  for key in bool_keys:
      params[key] = params[key].lower() == "true"

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



def main():
  args=pares_args()
  config = configparser.ConfigParser()
  config.read(args.config_path)
  database_path = config['PATH LIST']['database-path']
  cifdir = config['PATH LIST']['cifdir']
  params,n_jobs,adjacent_num = load_params_from_config(config)
  adjacency_algorithm = params.pop('adjacency_algorithm')
  max_neib = params.pop('max_neib')
  params.update({'databasepath':database_path})
  result_base_path = f'result/{cifdir}'
  import shutil
  #既存のディレクトリがある場合は削除
  if os.path.isdir(result_base_path):
      shutil.rmtree(result_base_path)

  #cifから隣接情報の取出し
  if adjacency_algorithm == 'neib':
    from Distance_based_on_Cluster_Analysis.make_nn_data_from_fortran import CIFDataProcessor
    maker = CIFDataProcessor(max_neib = max_neib,algorithm='pymatgen')
    maker.make_nn_data_from_cifdirs(cifdir,'result')
  elif adjacency_algorithm == 'chemenv':
      run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
      run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
  
  print('ok')
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

  #各cifファイルの特徴量を計算
  print('load database')
  characteriz_func=CrystalFeatureCalculator(**params)
  print('ok')

  #特徴量の計算
  result_cifdirs = [os.path.join(result_base_path,cifid) for cifid in cifid_list]
  with tqdm_joblib(len(result_cifdirs)):
    Parallel(n_jobs=n_jobs)([delayed(parallel_calculate_feature)(path,characteriz_func) for path in result_cifdirs])

  #各cifファイルの特徴量を結合

  point_files = glob.glob(f'{result_base_path}/*/cifpoint')
  point_df = [pd.read_csv(file_i) for file_i in point_files]
  point_df = pd.concat(point_df)
  point_df.to_csv(f'{result_base_path}/cifpoint',index=False)

if __name__=='__main__':
  main()