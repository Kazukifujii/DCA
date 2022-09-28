from crystal_emd.read_info import remake_csv



adress='result/testcif/ABW/ABW_0_0.csv'''
#出力するファイルの名前とディレクトリは変更可能：remake_csv(adress,outname='test.csv')

#outnameを指定しないとcsvファイルが存在するディレクトリにSi_ABW_0_0.csvという名前で出力される
remake_csv(adress)