import pickle

with open('main_log.pickle','rb') as f:
	log=pickle.load(f)

import copy 

txtlog="".join(log)
import re
loglist=re.split('\n',txtlog)
logindex=list()
for i,txt in enumerate(loglist):
	if not re.match('(OSO)',txt):
		continue
	#print('{} {}'.format(i,txt))
	logindex.append(i)

for id in logindex:
	#rint(loglist[int(id):int(id+20)])
	#print()
	break

import pandas as pd
dir='/home/fujikazuki/crystal_emd/result/allzeorite'
outcsvname='all_distance.csv'
picadress=pd.read_csv('{}/allcif_cluster'.format(dir),index_col=0)
import subprocess

for i in picadress.adress.to_list():
	result=subprocess.getoutput('ls {}/*_0_0.csv'.format(i))
	cifid=re.split('/',i)[-1]
	if len(result)==101:
		continue
	print('{}  {}'.format(cifid,len(result)))