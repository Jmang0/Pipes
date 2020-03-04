import csv
from pynode.main import *

with open("pipes.csv","r") as f:
    data = list(csv.reader(f))[1:]

header = ['Node 1', 'Node 2', 'length', 'diameter', 'material', 'year', \
'elasticity', 'wall_thickness', 'poissions_ratio', 'Kr', 'wave_speed']

def run():
    for i in range(15):
        graph.add_node(str(i+1))

    for row in data:
        edge = Edge(row[0],row[1],weight=row[-1]+'m/s')
        for i in range(len(row)-2):
            edge.set_attribute(header[i],row[i])
        graph.add_edge(edge)

begin_pynode(run)
