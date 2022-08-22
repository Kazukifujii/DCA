
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
def clusterplot(clusterdf,title='cluster.png'):
	noods=list()
	for index,i in clusterdf.iterrows():
		if index==0:
			continue
		front_idx=i.loc['front_index']
		a=clusterdf.loc[front_idx].loc['x':'z']
		b=i.loc['x':'z']
		noods.append(([a.x,b.x],[a.y,b.y],[a.z,b.z]))
	fig = plt.figure(figsize = (12, 12))
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(clusterdf.x,clusterdf.y,clusterdf.z)
	for index,i in clusterdf.iterrows():
		ax.text(i.x,i.y,i.z,i.atom)
	for nood in noods:
		line = art3d.Line3D(*nood)
		ax.add_line(line)
	fig.savefig(title)
	plt.close()
	