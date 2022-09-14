from dataclasses import replace
from turtle import Turtle
from distance_func import make_distance

csv1='result/testcif/ABW/ABW_0_0.csv'
csv2='result/testcif/ABW/ABW_2_0.csv'

val=make_distance(csv1,csv2,values=True)

print(val)
