from subprocess import run
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
import argparse,os
import pickle
import glob
import pandas as pd
from joblib import Parallel, delayed
from Distance_based_on_Cluster_Analysis.characterization import CrystalFeatureCalculator
def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--cifdir',default='cifdirs/sort_volume_ciffiles_top_100',help='zeolitecif')
    pares.add_argument('--adjacent_num',default=2,help='(int)')
    pares.add_argument('--database_path',default='cluster_database',help='database path')
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
  


def main():
  pares=pares_args()
  cifdir=pares.cifdir
  adjacent_num=int(pares.adjacent_num)
  databaseaddress=pares.database_path
  resultdir=os.path.join('result',cifdir)
  #cifから隣接情報の取出し
  run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
  print('emd make_adjacent_tabel')
  run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
  print('ok')

  #隣接情報からクラスターを生成
  print('make cluster dataset')
  picdata=make_sort_ciffile(resultdir,estimecont='all')
  Parallel(n_jobs=-1)([delayed(parallen_make_cluster_dataset)(data,adjacent_num) for _,data in picdata.iterrows()])
  print('ok')
  #各cifファイルの特徴量を計算
  characteriz_func=CrystalFeatureCalculator(databaseaddress)

  #特徴量の計算
  Parallel(n_jobs=-1)([delayed(parallel_calculate_feature)(data,characteriz_func) for _,data in picdata.iterrows()])

  #各cifファイルの特徴量を結合

  point_files = glob.glob(f'{resultdir}/*/cifpoint')
  point_df = [pd.read_csv(file_i) for file_i in point_files]
  point_df = pd.concat(point_df)
  point_df.to_csv(f'{resultdir}/cifpoint',index=False)

if __name__=='__main__':
  main()