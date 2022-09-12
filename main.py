import subprocess

log=list()

log0= subprocess.getoutput("python3 make_sort_ciffile.py")
print('end make_sort_ciffile')
log.append(log0)
#log1= subprocess.getoutput("python3 make_self_distance.py")
#rint('end_self_distance')
#log.append(log1)
log2=subprocess.getoutput("python3 make_self_clustering.py")
print("end_self_clustring")
log.append(log2)
log3= subprocess.getoutput("python3 make_picup_cluster.py")
print("end_picup")
log.append(log3)
log4= subprocess.getoutput("python3 make_all_distance.py")
log.append(log4)
import pickle
with open(("main_log.pickle"),"wb") as fwb:
    pickle.dump(log,fwb)