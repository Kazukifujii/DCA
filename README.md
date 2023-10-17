### データベースとなるcifファイルについて  
  ゼオライト学会で用意されているcifファイルをget_zeolitecif.pyを実行して取得した(最終取得日:2023年10月12日)  
  また、ここで取得したcifファイルは後にcif2cellを通すことになっている。  
  その際、うまく変換できないファイルが4つほど存在したのでpymatgenを使ってそれぞれ下記のようなの整形作業を行った。  

1. JOZ,SAF,SEWは'_symmetry_space_group_name_H-M'の項目をcif2cellがうまく読み込めなかったのでpymatgenを使って該当項目の再定義を行った


```python
from pymatgen.io.cif import CifParser, CifWriter
import os
cifids = ['JOZ','SAF','SEW']
filepath = 'datas/cifdirs/allzeolite'
for cifid in cifids:
    path = os.path.join(filepath,cifid+'.cif')
    cifparser = CifParser(path)
    structure = cifparser.get_structures()[0]
    #poscarを使ってciffileを書き出す
    cifwriter = CifWriter(structure,symprec=0.001)
    cifwriter.write_file(path)
```

2. RSNでは'Si'と記述されるべき所、'T'との記述に置き換わっていたのでその部分を書き換えた


```python
path = os.path.join(filepath,'RSN.cif')
cifparser = CifParser(path)
structure = cifparser.get_structures()[0]
structure.replace_species({'T':'Si'})
cifwriter = CifWriter(structure,symprec=0.1)
cifwriter.write_file(path)
```
