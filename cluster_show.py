from read_info import clusterplot as clp
import os
import sys
import argparse
import subprocess
import pandas as pd


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-csvn')
	parser.add_argument('-e','--explanation', default=False)
	args = parser.parse_args()

	if args.explanation:
		print('''-csvn : /cluster_0_0.csv''')
		sys.exit()
	df=pd.read_csv(args.csvn,index_col=0)
	clp(df,show=True,save=False)

if __name__ == '__main__':
	main()