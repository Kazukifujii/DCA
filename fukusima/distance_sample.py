from test_distance_func import make_distance
csv1='/home/fujikazuki/crystal_emd/result/testcif/ABW/ABW_0_0.csv'
csv2='/home/fujikazuki/crystal_emd/result/testcif/ABW/ABW_1_0.csv'

dis=make_distance(csv1,csv2)
print(dis)