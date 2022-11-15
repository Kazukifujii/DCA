import sys,re,argparse,os
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from .distance_func import cal_distance
from copy import deepcopy
from glob import glob
def change(csv1,csv2):
    #print(os.getcwd())
    #sys.exit()
    csvadress1=csv1
    csvadress2=csv2
    csv1=pd.read_csv(csv1,index_col=0)
    csv2=pd.read_csv(csv2,index_col=0)
    x=csv1['x']
    y=csv1['y']
    z=csv1['z']
    isite=csv1['isite']
    atom=csv1['atom']
    
    u=csv2['x']
    v=csv2['y']
    w=csv2['z']
    isite2=csv2['isite']
    atom2=csv2['atom']
    
    val=cal_distance(csvadress1,csvadress2,values=True)
    u2=[]
    v2=[]
    w2=[]
    isite3=[]
    atom3=[]
    for i in range(len(val)):
        a=re.sub(r"\D","",val[i][0][-2:])
        u2.append(u[int(a)])
        v2.append(v[int(a)])
        w2.append(w[int(a)])
        isite3.append(isite2[int(a)])
        atom3.append(atom2[int(a)])

    #plt.style.use('ggplot')
    plt.rcParams["axes.facecolor"] = 'white'
    fig = plt.figure(figsize=(8, 8)) # 図の設定 
    ax = fig.add_subplot(projection='3d') # 3Dプロットの設定
    for i in range(len(x)):
        ax.quiver(x[i], y[i], z[i], u2[i]-x[i], v2[i]-y[i], w2[i]-z[i], arrow_length_ratio=0.1,color="red") # 矢印プロット
        ax.scatter(x[i], y[i], z[i], label='(x, y, z)',c="blue") # 始点
        ax.scatter(u2[i], v2[i], w2[i], label='(x+u, y+v, z+w)',c="green") # 終点
		#ax.set_xlabel('x')
		#ax.set_ylabel('y')
		#ax.set_zlabel('z')
        ax.set_title(csvadress1+'(blue) to ' +csvadress2+'(green)',size=10) # タイトル
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
    for i in range(len(x)):
        text=str(atom[i])+'_'+str(isite[i])
        #text=str(isite[0])+'_'+str(isite[i])
		#text='ABW_'+str(isite[0])+'_'+str(isite[i])
        text2=str(atom3[i])+'_'+str(isite3[i])
		#text2=str(isite2[0])+'_'+str(isite3[i])
		#text2='ABW_'+str(isite2[0])+'_'+str(isite3[i])
        ax.text(x[i],y[i],z[i],text,size=8)
        ax.text(u2[i],v2[i],w2[i],text2,size=8)

    noods=list()
    for index,i in csv1.iterrows():
        if index==0:
            continue
        front_idx=i.loc['front_index']
        a=csv1.loc[front_idx].loc['x':'z']
        b=i.loc['x':'z']
        noods.append(([a.x,b.x],[a.y,b.y],[a.z,b.z]))
    for nood in noods:
        line = art3d.Line3D(*nood)
        ax.add_line(line)

    plt.show()


def double_clusterplot(clusterdf1,clusterdf2,title='cluster.png',show=None,save=True):
    noods=list()
    fig = plt.figure(figsize = (12, 12))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    for clusterdf in [clusterdf1,clusterdf2]:
        for index,i in clusterdf.iterrows():
            if index==0:
                continue
            front_idx=i.loc['front_index']
            a=clusterdf.loc[front_idx].loc['x':'z']
            b=i.loc['x':'z']
            noods.append(([a.x,b.x],[a.y,b.y],[a.z,b.z]))
        ax.scatter(clusterdf.x,clusterdf.y,clusterdf.z)
        for index,i in clusterdf.iterrows():
            text=i.atom+'_'+str(int(i.isite))
            ax.text(i.x,i.y,i.z,text)
        for nood in noods:
            line = art3d.Line3D(*nood)
            ax.add_line(line)
        fig.suptitle(title)
        if save:
            fig.savefig(title)
        if show:
            plt.show()
        plt.close()
from PIL import Image
class DrawGif():
    def __init__(self):
        self.image=list()
    def set_data(self,clusterdf1,clusterdf2):
        pngname='cluster.png'
        double_clusterplot(clusterdf1,clusterdf2,title=pngname)
        self.image.append(Image.open(pngname))
        os.remove(pngname)
        return
    def makegif(self,filename='clustergif.gif'):
        self.image[0].save(filename,save_all=True, append_images=self.image[1:],optimize=False, duration=500, loop=0)
        return

def distance_histgram(cifdir,database_adress='database',show=False,save=True):
    distanlist=glob('{}/*distance'.format(cifdir))
    histdf=pd.DataFrame()
    for dataadress in distanlist:
        data=pd.read_csv(dataadress,index_col=0).iloc[0]
        clusteradress_base='{}/{}_{}.csv'.format(database_adress,data.isite_j,data.pattern_j)
        clusteradress_cif='{}/{}_{}.csv'.format(cifdir,data.isite_i,data.pattern_i)
        d=cal_distance(csv_adress1=clusteradress_cif,csv_adress2=clusteradress_base,histgram=True)
        d.sort(reverse=True)
        histdf.loc[:,'{}_{}'.format(data.isite_i,data.isite_j)]=deepcopy(d)
    histdf=histdf.sort_index(axis=1)
    histdf.plot(kind='bar')
    if show:
        plt.show()
    if save:
        plt.savefig('{}/{}_move.png'.format(cifdir,data.isite_i))
    return