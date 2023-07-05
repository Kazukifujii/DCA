from subprocess import run
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
import argparse,os
import pickle
from Distance_based_on_Cluster_Analysis.characterization import CrystalFeatureCalculator
def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--cifdir',default='cifdirs/sort_volume_ciffiles_top_100',help='zeolitecif')
    pares.add_argument('--adjacent_num',default=2,help='(int)')
    pares.add_argument('--database_path',default='cluster_database',help='database path')
    return pares.parse_args()

def main():
  pares=pares_args()
  cifdir=pares.cifdir
  adjacent_num=int(pares.adjacent_num)
  databaseaddress=pares.database_path
  #cifから隣接情報の取出し
  run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
  print('emd make_adjacent_tabel')
  run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
  print('emd make_nn_data')

  #隣接情報からクラスターを生成
  picdata=make_sort_ciffile('result/{}'.format(cifdir),estimecont='all')
  allciflen=picdata.shape[0]
  for i in range(len(picdata)):
      data=picdata.iloc[i,:]
      print('\r{} {}/{}'.format(data.cifid,i+1,allciflen),end='')
      nn_data_address= os.path.join(data.cifaddress,f"nb_{data.cifid}.pickle")
      make_cluster_dataset(cifid=data.cifid,nn_data_address=nn_data_address,adjacent_num=adjacent_num,rotation=False,outdir=data.cifaddress)
  print()

  #計算結果の保存
  resulttxt='result/{}/cifpoint'.format(cifdir)
  text_file=open(resulttxt,'w')
  text_file.write('cifid,point\n')
  text_file.close()

  #各cifファイルの特徴量を計算
  characteriz_func=CrystalFeatureCalculator(databaseaddress)
  for i in range(len(picdata)):
    data = picdata.iloc[i,:]
    cifid=os.path.basename(data.cifaddress)
    print('cif {}/{}'.format(i+1,len(picdata)))
    print(cifid)
    feature = characteriz_func.calculate_features(data.cifaddress)
    text_file=open(resulttxt,'a')
    text_file.write('{},{}\n'.format(cifid,feature))
    text_file.close()
    #計算ログの保存
    
    for j,log in enumerate(characteriz_func.calculate_log):
      pickle.dump(log,open(f'result/{cifdir}/log/{cifid}_{j}.pickle','wb'))
if __name__=='__main__':
  main()