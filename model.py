import csv
from pynode.main import *

f = open("pipes.csv","r")
data = list(csv.reader(f))
f.close()

header = data[0]
data = data[1:]

print(header)
def run():
    for i in range(15):
        graph.add_node(str(i+1))

    for row in data:
        edge = Edge(row[0],row[1])
        for i in range(len(row)-2):
            edge.set_attribute(header[i],row[i])
        graph.add_edge(edge)

begin_pynode(run)
