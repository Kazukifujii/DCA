1. Distance based on Cluster Analysis(DCA)  
  複数の実験データを元に結晶の予測構造を幾何学的に評価します.
   
2. プロジェクトの説明  
  結晶構造予測分野は非常にニーズの高い研究分野であり,分子動力学など数理的手法や遺伝アルゴリズムなどの手法を中心に予測された結晶構造がインターネット上に公開されている.しかし,予測された構造は大量に存在する上,非現実的な構造も含まれているため非常に扱いづらい情報となってしまっている.  
  そこで本プロジェクトでは,実験から得られた構造を元に、それらの予測構造を幾何学的な特徴量で定量的に評価を行うことにした.  
  評価方法については事項で説明する.  

3. 評価方法  
  結晶構造は局所構造の組み合わせて構成されてたものと仮定した上で,次のプロセスで予測構造を評価している.  
  1. 局所構造の定義として、任意の原子中心に一定の隣接数を基準に切り出した原子の集合体(以後クラスターと呼ぶ)  
  2. ユニットセル内に存在するクラスターをすべて取り出す  
  3. Earth Mover's Distance(EMD)使用して予測構造のクラスターと実験データのクラスターを定量的に比較  
  4. 3で行った定量的評価を2で取り出したクラスター全てに適用し、その平均値を予測構造の最終的な評価値とする.  

1. プロジェクトの使用方法  
   
2. 補足事項(現在把握している問題と今後の開発で解決するかどうか、または解決する順番等を記載する)






# 概要  
  本プログラムは結晶の予測構造に対し、実験データを元に再評価を行っている。

## 実験データについて  

  ゼオライト学会で用意されているcifファイルをget_zeolitecif.pyを実行して取得し、いくつかの整形作業を行った後新たにデータベースとしてディレクトにまとめた。  
  行った作業は以下の3項目  
  1. ユニットセル内に存在する組成比がになっていないものの除外  
    ```python3  
      import os
      import shutil
      import glob
      from pymatgen.core.composition import Composition
      from pymatgen.io.cif import CifParser

      cif_paths = glob.glob('zeolitecifs/*.cif')
      del_list = []
      for path in cif_paths:
          # Create a CifParser object from the CIF file
          parser = CifParser(path)
          # Get the crystal structure from the CifParser object
          structure = parser.get_structures()[0]
          # Get the composition from the crystal structure
          comp = Composition.from_dict(structure.composition.as_dict())
          # Get the composition ratio
          ratio = comp.get_el_amt_dict()
          # Print the composition ratio
          
          #check if only Si and O
          if len(ratio) == 2 and 'Si' in ratio and 'O' in ratio:
              #check if Si/O ratio is 1/2
              if ratio['Si']/ratio['O'] == 0.5:
                  continue
          del_list.append(path)
      #move files to another directory

      #make new directory
      if os.path.isdir('anomalycifs'):
          shutil.rmtree('anomalycifs')
      os.mkdir('anomalycifs')

      for path in del_list:
          shutil.move(path,'anomalycifs')
    ```  
  2. 一部cifファイルのsymmetry_space_group_name_H-Mを一部書き換え  
    JOZ,SAF,SEWは'_symmetry_space_group_name_H-M'の項目をcif2cellがうまく読み込めなかったのでpymatgenを使って該当項目の再定義を行った  

    ```python3  
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
  3. cifのフォーマットに沿っていないファイルの一部書き換え  
    RSNでは'Si'と記述されるべき所、'T'との記述に置き換わっていたのでその部分を書き換えた  
    ```python3  
    path = os.path.join(filepath,'RSN.cif')
    cifparser = CifParser(path)
    structure = cifparser.get_structures()[0]
    structure.replace_species({'T':'Si'})
    cifwriter = CifWriter(structure,symprec=0.1)
    cifwriter.write_file(path)
    ```
