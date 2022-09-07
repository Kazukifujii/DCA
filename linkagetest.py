import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
df = pd.DataFrame(np.random.rand(16*21).reshape(21,16))
Z = linkage(df,method='ward',metric='euclidean')
t = 0.7*max(Z[:,2])
print(t)
#c = fcluster(Z, t, criterion='distance')
# t:クラスタリングするユーグリッド距離の基準
# この場合、ユークリッド距離の最も離れている一番上の水平線の70%の位置をクラスタリングの基準とする