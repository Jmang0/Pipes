import csv
from pynode.main import *

with open("pipes.csv","r") as f:
    data = list(csv.reader(f))[1:]

sensor_no = 1

def run():
    global text, node1, node2
    # Add nodes
    for i in range(15):
        node = Node(str(i+1))
        node.set_attribute('sensor',False)
        graph.add_node(node)

    # Add edges
    for row in data:
        edge = Edge(row[0],row[1])

        edge.set_attribute('length',row[2])
        edge.set_attribute('material',row[4])
        edge.set_attribute('year',row[5])
        edge.set_attribute('elasticity',row[6])
        edge.set_attribute('wall_thickness',row[7])
        edge.set_attribute('possians_ratio',row[8])
        edge.set_attribute('wave_speed',row[10])

        time = float(row[2])/float(row[10]) #time = distance/speed
        edge.set_attribute('wave_time',time)

        edge.set_weight(edge.attribute('length'))

        graph.add_edge(edge)


    print('--- Adding Sensors ---')
    print('Click start of pipe')
    register_click_listener(n1)

def  _(n):
    return None

def n1(node):
    # if node.value().startswith('Sensor'):
    #     print('Invalid choice')

    global node1
    node1 = node
    node1.highlight(Color.YELLOW,20)
    print('Click end of pipe')
    register_click_listener(n2)

def n2(node):
    # if node.value().startswith('Sensor'):
    #     print('Invalid choice')


    global node1, node2, sensor_no
    node2 = node

    if graph.adjacent(node1,node2):
        node2.highlight(Color.YELLOW,15)
        pipe = graph.edges_between(node1,node2)[0]
        print(f'How far from {node1} is the break?')
        total = float(pipe.weight())
        length1 = float(input(f'Enter a distance between 0 and {total} meters: '))
        while not (0 <= length1 <= total):
            length1 = float(input(f'Enter a distance between 0 and {total} meters: '))
        length2 = round(total-length1,1)

        graph.remove_edge(pipe)

        sensor = Node(f'Sensor {sensor_no}')
        sensor_no += 1
        sensor.set_color(Color.GREEN)
        graph.add_node(sensor)

        graph.add_edge(node1,sensor,weight=length1)
        graph.add_edge(sensor,node2,weight=length2)

        register_click_listener(_)

        if input('Add another sensor? (y/n) ') == 'y':
            print('Click start of pipe')
            register_click_listener(n1)
    else:
        print('Junctions must be adjacent, choose the end of the pipe again')

begin_pynode(run)
