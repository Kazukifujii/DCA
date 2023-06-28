from subprocess import run
import os,subprocess
from Distance_based_on_Cluster_Analysis.distance import cal_distances
from Distance_based_on_Cluster_Analysis.clustering_func import make_clustering
from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
from Distance_based_on_Cluster_Analysis.cluster_adress_func import ClusterManager,fcluster_list
import argparse

def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--cifdir',default='cifdirs/allzeolite',help='zeolitecif')
    pares.add_argument('--adjacent_num',default=2,help='(int)')
    pares.add_argument('--cluster_atom_num',default=8,help='(int)')
    pares.add_argument('--outdirname',default='cluster_database')
    return pares.parse_args()

def main():
    pares=pares_args()
    cifdir=pares.cifdir
    adjacent_num=int(pares.adjacent_num)
    cluster_atom_num=int(pares.cluster_atom_num)
    database=pares.outdirname

    #cifから隣接情報の取出し
    """run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
    run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
    """#隣接情報からクラスターを生成
    picdata=make_sort_ciffile(f'result/{cifdir}',estimecont='all')
    cwd = os.getcwd()
    allciflen=picdata.shape[0]

    for i,data in picdata.iterrows():
        print(f'\r{data.cifid} {i+1}/{allciflen}',end='')
        nn_data_adress= subprocess.getoutput(f"find {data.cifadress} -name nb_*.pickle")
        make_cluster_dataset(cifid=data.cifid,adjacent_num=adjacent_num,nn_data_adress=nn_data_adress,outdir=data.cifadress,rotation=False)
    print('')
    #壊れているクラスターの削除
    
    cm=ClusterManager.read_cluster_list(f'result/{cifdir}',dirs=True)
    f=open('clean up_cluster.log','w')
    for i in range(len(cm.cluster_list)):
        data=cm.cluster_list[i]
        clusteradress=f'{data.adress}/{data.cifid}_{data.isite}_0.csv'
        if not os.path.isfile(clusteradress):
            print('no file',clusteradress)
            continue
        index_num=int(open(clusteradress,'r').readlines()[-1][0])
        if index_num!=cluster_atom_num:
            f.write(f'{clusteradress}\n')
            os.remove(clusteradress)
    f.close()

    #残っているクラスターの回転パターンを全て取る
    cm=ClusterManager(f'result/{cifdir}',dirs=True)
    for i in range(len(cm.cluster_list)):
        data=cm.cluster_list[i]
        clusteradress=f'{data.adress}/{data.cifid}_{data.isite}_0.csv'
        make_cluster_dataset(cluster_adress=clusteradress,outdir=data.adress)
    print('')

    #各結晶に属するクラスターの距離を計算(等価なクラスターを取り出すため)

    for i in range(len(picdata)):
        data=picdata.iloc[i]
        cifid=data.cifid
        print(cifid)
        targetcluster=ClusterManager(data.cifadress)
        #距離の計算
        cluster_distance_df=cal_distances(targetcluster)
        #クラスタリングによる分類
        flusterdf=make_clustering(cluster_distance_df)
        flusterdf.to_csv(f"{data.cifadress}/{cifid}_fcluster")
    #等価なクラスターをリストアップし、一つのディレクトリにまとめる(データベースの作成)
    fcluster_df=fcluster_list(f'result/{cifdir}')
    import shutil

    if os.path.isdir(database):
        shutil.rmtree(database)
    os.mkdir(database)

    for i,data in fcluster_df.iterrows():
        for pattern in range(12):
            clusteradress=f'{data.adress}/{data.cifid}_{data.isite}_{pattern}.csv'
            if not os.path.isfile(clusteradress):
                print('not file ',clusteradress)
            copyadress=f'{database}/{data.cifid}_{data.isite}_{pattern}.csv'
            shutil.copy(clusteradress,copyadress)

if __name__=='__main__':
    main()
