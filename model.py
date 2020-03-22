import csv
from pynode.main import *
from random import random

with open("pipes.csv","r") as f:
    data = list(csv.reader(f))[1:]

def get_attributes(edge):
    attrs = ['material','year','elasticity','wall_thickness','possians_ratio','wave_speed','wave_time']
    return {attr: edge.attribute(attr) for attr in attrs}

def insert_node(middle_node,edge):
    node1 = edge.source()
    node2 = edge.target()
    total = float(edge.weight())

    # Get user input on where the node should be inserted
    print(f'How far from {node1} is the sensor?')
    inp = input(f"Enter a distance between 0 and {total} meters, 'half' or 'random': ")
    if inp == 'half':
        length1 = total/2
    elif inp == 'random':
        length1 = round(total*random(),2)
    else:
        length1 = float(inp)

    while not (0 <= length1 <= total):
        length1 = float(input(f'Enter a distance between 0 and {total} meters: '))
    length2 = round(total-length1,2)

    # Create the 2 edges
    graph.add_node(middle_node)
    e1 = Edge(node1,middle_node,weight=length1)
    e2 = Edge(middle_node,node2,weight=length2)

    # Transfer the attributes
    for name, value in get_attributes(edge).items():
        e1.set_attribute(name,value)
        e2.set_attribute(name,value)

    # Remove the old edge, add the new edges
    graph.remove_edge(edge)
    graph.add_edge(e1)
    graph.add_edge(e2)

def run():
    global text, node1, node2, sensor_no
    sensor_no = 1

    # Add nodes
    for i in range(15):
        node = Node(str(i+1))
        graph.add_node(node)

    # Add edges
    for row in data:
        edge = Edge(row[0],row[1],weight=row[2])

        edge.set_attribute('flowed',False)

        edge.set_attribute('material',row[4])
        edge.set_attribute('year',row[5])
        edge.set_attribute('elasticity',row[6])
        edge.set_attribute('wall_thickness',row[7])
        edge.set_attribute('possians_ratio',row[8])
        edge.set_attribute('wave_speed',row[10])

        time = float(row[2])/float(row[10]) #time = distance/speed
        edge.set_attribute('wave_time',time)

        graph.add_edge(edge)

    print('--- Adding Sensors ---')
    print('Click start of pipe')
    register_click_listener(sensor1)


def  _(node):
    return None

def sensor1(node):
    global node1
    node1 = node
    node1.highlight(Color.YELLOW,20)
    print('Click end of pipe')
    register_click_listener(sensor2)

def sensor2(node):
    global node1, node2, sensor_no
    node2 = node

    if graph.adjacent(node1,node2):
        # Animation
        node1.highlight(Color.YELLOW,20)
        node2.highlight(Color.YELLOW,20)

        # Inserting the sensor
        pipe = graph.edges_between(node1,node2)[0]
        sensor = Node(f'Sensor {sensor_no}')
        sensor_no += 1
        sensor.set_color(Color.GREEN)

        insert_node(sensor,pipe)

        # Disable click function
        register_click_listener(_)

        # Check whther to add another sensor
        print()
        if input('Add another sensor? (y/n) ') == 'y':
            print('Click start of pipe')
            register_click_listener(sensor1)
        else:
            print('Where do you want the break?')
            print('Click start of pipe')
            register_click_listener(break1)

    else:
        print('Junctions must be adjacent, choose the end of the pipe again')


def break1(node):
    global node1
    node1 = node
    node1.highlight(Color.RED,20)
    print('Click end of pipe')
    register_click_listener(break2)

def break2(node):
    global node1, node2, sensor_no
    node2 = node

    if graph.adjacent(node1,node2):
        # Animation
        node1.highlight(Color.RED,20)
        node2.highlight(Color.RED,20)

        # Inserting the break
        pipe = graph.edges_between(node1,node2)[0]
        brek = Node('BREAK')
        brek.set_color(Color.RED)

        insert_node(brek,pipe)

    else:
        print('Junctions must be adjacent, choose the end of the pipe again')

begin_pynode(run)
