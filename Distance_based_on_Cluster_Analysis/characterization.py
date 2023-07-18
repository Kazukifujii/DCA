import numpy as np
from Distance_based_on_Cluster_Analysis.clustermanager import ClusterManager
from Distance_based_on_Cluster_Analysis.clustermanager import DCAFormatManager
from Distance_based_on_Cluster_Analysis.distance import cal_distances

class ClusterFeatureCalculator():
    def __init__(self, databasepath):
        self.format_manager = DCAFormatManager.from_dirpath(databasepath)
    
    def cluster_calculate_features(self,clusterpath):
        self.format_manager.calculate_cluster_featuring(clusterpath=clusterpath)
        self.distance = cal_distances(self.format_manager)
        return self.distance.sort_values('distance').reset_index(drop=True).loc[0,'distance']


class CrystalFeatureCalculator(ClusterFeatureCalculator):
    def __init__(self, databasepath):
        super().__init__(databasepath)
    
    def calculate_features(self,crystalpath,method = 'mean'):
        clustermanager = ClusterManager.from_dirpath(crystalpath)
        result = list()
        self.calculate_log = list()
        for i in range(len(clustermanager.cluster_list_df)):
            cluster_data = clustermanager.cluster_list_df.iloc[i]
            features = self.cluster_calculate_features(cluster_data)
            result.append(features)
            self.calculate_log.append(self.distance.copy())
        
        if method == 'mean':
            return np.mean(result)
        elif method == 'max':
            return np.max(result)