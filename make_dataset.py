from subprocess import run
import os,subprocess

cifdir="testcif"
adjacent_num=2
cluster_atom_num=8
database='cluster_database'
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
    adjacent_num=pares.adjacent_num
    cluster_atom_num=pares.cluster_atom_num
    database=pares.outdirname

    #cifから隣接情報の取出し
    run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
    print('emd make_adjacent_tabel')
    run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
    print('emd make_nn_data')

    #隣接情報からクラスターを生成
    from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
    from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
    picdata=make_sort_ciffile('result/{}'.format(cifdir),estimecont='all')
    cwd = os.getcwd()
    allciflen=picdata.shape[0]

    for i,data in picdata.iterrows():
        print('\r{} {}/{}'.format(data.cifid,i+1,allciflen),end='')
        nn_data_adress= subprocess.getoutput("find {0} -name nb_*.pickle".format(data.cifadress))
        make_cluster_dataset(cifid=data.cifid,adjacent_num=adjacent_num,nn_data_adress=nn_data_adress,outdir=data.cifadress)
    print('')
    #壊れているクラスターの削除

    from Distance_based_on_Cluster_Analysis.cluster_adress_func import cluster_list
    listdf=cluster_list('result/{}'.format(cifdir),dirs=True)
    f=open('clean up_cluster.log','w')
    for i,data in listdf.iterrows():
        clusteradress='{}/{}_{}_0.csv'.format(data.adress,data.cifid,data.isite)
        if not os.path.isfile(clusteradress):
            print('no file',clusteradress)
            continue
        index_num=int(open(clusteradress,'r').readlines()[-1][0])
        if index_num!=cluster_atom_num:
            f.write('{}\n'.format(clusteradress))
            os.remove(clusteradress)
    f.close()

    #残っているクラスターの回転パターンを全て取る



    #各結晶に属するクラスターの距離を計算(等価なクラスターを取り出すため)
    from Distance_based_on_Cluster_Analysis.cluster_adress_func import isite_list
    from Distance_based_on_Cluster_Analysis.distance_func import make_distance_csv,remake_distance
    from Distance_based_on_Cluster_Analysis.clustering_func import make_clusering
    cont=0

    for i,data in picdata.iterrows():
        cifid=data.cifid
        print(cifid)
        listadress_=isite_list(data.cifadress)
        #距離の計算
        make_distance_csv(listadress=listadress_,resultname="{}/{}_self_distance".format(data.cifadress,cifid))
        #10*-8以下の値を0に近似
        remake_distance("{}/{}_self_distance".format(data.cifadress,cifid))
        #クラスタリングによる分類
        flusterdf=make_clusering(csvadress="{}/{}_self_distance_remake".format(data.cifadress,cifid),csvn="{}/{}_sort_distance".format(data.cifadress,cifid),pngn='{}/{}_self_distance.png'.format(data.cifadress,cifid))
        flusterdf.to_csv("{}/{}_fcluster".format(data.cifadress,cifid))

    #等価なクラスターをリストアップし、一つのディレクトリにまとめる
    from Distance_based_on_Cluster_Analysis.cluster_adress_func import fcluster_list
    fclusterdf=fcluster_list('result/{}'.format(cifdir))
    import shutil

    if os.path.isdir(database):
        shutil.rmtree(database)
    os.mkdir(database)

    for i,data in fclusterdf.iterrows():
        for pattern in range(12):
            clusteradress='{}/{}_{}_{}.csv'.format(data.adress,data.cifid,data.isite,pattern)
            if not os.path.isfile(clusteradress):
                print('not file ',clusteradress)
            copyadress='{}/{}_{}_{}.csv'.format(database,data.cifid,data.isite,pattern)
            shutil.copy(clusteradress,copyadress)

if __name__=='__main__':
    main()
