import re
d=open('init_POSCARS','r').readlines()
idlist=list()
for I,i in enumerate(d):
    if re.match('ID',i):
        idlist.append(I)

for I,i in enumerate(idlist):
    idname=d[idlist[I]].replace('\n','')
    if int(len(idlist)-1)==I:
        poscar=d[idlist[I]::]
        f=open('{}_POSCAR'.format(idname),'w')
        f.writelines(poscar)
        f.close()
        continue
    poscar=d[idlist[I]:idlist[I+1]]
    f=open('{}_POSCAR'.format(idname),'w')
    f.writelines(poscar)
    f.close()