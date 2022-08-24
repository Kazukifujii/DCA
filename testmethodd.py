import os,pickle
import subprocess
from read_info import Set_Cluster_Info
import copy



from read_info import clusterplot as clp
import re
cifdir_ = subprocess.getoutput("find {0} -type d | sort".format('result/cod'))
cifdir = cifdir_.split('\n')
del cifdir[0]

cwd = os.getcwd()
for i in cifdir:
	