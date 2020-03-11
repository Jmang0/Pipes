import csv
from pynode.main import *

with open("pipes.csv","r") as f:
    data = list(csv.reader(f))[1:]

header = ['Node 1', 'Node 2', 'length', 'diameter', 'material', 'year', \
'elasticity', 'wall_thickness', 'poissions_ratio', 'Kr', 'wave_speed']

def run():
    # Add nodes
    for i in range(15):
        node = Node(str(i+1))
        node.set_attribute('sensor',False)
        graph.add_node(node)

    # Add edges
    for row in data:
        edge = Edge(row[0],row[1],weight=row[-1]+'m/s')
        for i in range(len(row)-2):
            edge.set_attribute(header[i],row[i])
        graph.add_edge(edge)

    graph.add_node('text')


def add_sensor(node):
    if node.attribute('sensor'):
        node.set_attribute('sensor',False)
        node.set_color(Color.DARK_GREY)

    else:
        node.set_attribute('sensor',True)
        node.set_color(Color.GREEN)

begin_pynode(run)

register_click_listener(add_sensor)
