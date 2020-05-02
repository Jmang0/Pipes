import csv
from pynode.main import *
from random import random
from time import time
from copy import deepcopy

slowmo = 10 # Speed to show propogation at
testing = False #If testing is True, it skips user typing input

#---------- MODEL ----------
# Open data
with open("pipes.csv","r") as f:
    data = list(csv.reader(f))[1:]

def insert_node(middle_node,edge,name):
    node1 = edge.source()
    node2 = edge.target()
    total = float(edge.weight())

    while True:
        # Get user input on where the node should be inserted
        if not testing:
            print(f'How far from {node1} should the {name} be placed?')
            inp = input(f"Enter a distance between 0 and {total} meters, 'h' for half, or 'r' for random: ")

        try:
            #Check for all valid inputs, otherwise ask again
            if testing or inp == 'r':
                length1 = round(total*random(),2)
            elif inp == 'h':
                length1 = total/2
            elif 0 < float(inp) < total:
                length1 = float(inp)
            else:
                print('Invalid input, try again.')
                continue
        except:
            print('Invalid input, try again.')
            continue

        length2 = round(total-length1,2)
        break

    # Create the 2 edges
    graph.add_node(middle_node)
    e1 = Edge(node1,middle_node,weight=length1)
    e2 = Edge(middle_node,node2,weight=length2)

    # Transfer the attributes
    e1._attributes = deepcopy(edge._attributes)
    e2._attributes = deepcopy(edge._attributes)

    # Remove the old edge, add the new edges
    graph.remove_edge(edge)
    graph.add_edge(e1)
    graph.add_edge(e2)

def run():
    global text, node1, node2, sensor_no
    sensor_no = 1

    # Add nodes
    for i in range(15):
        graph.add_node(str(i+1))

    # Add edges
    for row in data:
        edge = Edge(row[0],row[1],weight=float(row[2]))

        edge.set_attribute('flowed',False)

        edge.set_attribute('material',row[4])
        edge.set_attribute('year',row[5])
        edge.set_attribute('elasticity',row[6])
        edge.set_attribute('wall_thickness',row[7])
        edge.set_attribute('possians_ratio',row[8])
        edge.set_attribute('wave_speed',float(row[10]))

        time = float(row[2])/float(row[10]) #time = distance/speed
        edge.set_attribute('wave_time',time)

        graph.add_edge(edge)

    print("Jai Mangos' Pipe Network Model")

    print('~ Adding Sensors ~')
    print('- Click 2 adjacent nodes or double click a single node')
    print()
    print('Click first node.')
    register_click_listener(sensor1)


def  _(node):
    return None

def sensor1(node):
    global node1
    node1 = node
    node1.highlight(Color.GREEN,20)
    print('Click second node.')
    register_click_listener(sensor2)

def sensor2(node):
    global node1, node2, sensor_no
    node2 = node

    node1.highlight(Color.GREEN,20)
    #If they are the same node
    if node1 == node2:
        sensor = node1
        sensor.set_value(f'Sensor {sensor_no}')

    #If they are adjacent
    elif graph.adjacent(node1,node2):
        # Animation
        node2.highlight(Color.GREEN,20)

        # Inserting the sensor
        pipe = graph.edges_between(node1,node2)[0]
        sensor = Node(f'Sensor {sensor_no}')
        insert_node(sensor,pipe,'sensor')

    else:
        print('Chosen nodes must be adjacent, choose the 2nd node again.')
        return None


    sensor_no += 1
    sensor.set_color(Color.GREEN)

    # Disable click function
    register_click_listener(_)

    # Check whther to add another sensor
    print()
    if not testing and input('Add another sensor? (y/n) ') == 'y':
        print('Click start of pipe.')
        register_click_listener(sensor1)
    else:
        print('Where do you want the break?')
        print('Click start of pipe.')
        register_click_listener(break1)


def break1(node):
    global node1
    node1 = node
    node1.highlight(Color.RED,20)
    print('Click 2nd node.')
    register_click_listener(break2)

def break2(node):
    global node1, node2, sensor_no, start_time
    node2 = node

    if graph.adjacent(node1,node2):
        # Animation
        node1.highlight(Color.RED,20)
        node2.highlight(Color.RED,20)

        # Inserting the break
        pipe = graph.edges_between(node1,node2)[0]
        brek = Node('BREAK')
        brek.set_color(Color.RED)

        insert_node(brek, pipe,'break')
        register_click_listener(_)

        #---------- ALGORITHM ----------
        start_time = time()
        spread(brek)

    else:
        print('Junctions must be adjacent, choose the end of the pipe again')


def spread(node):
    global start_time,slowmo

    # Visually indicate the water has reached this node
    node.highlight(color=Color.BLUE,size=node.size()*1.5)
    node.set_color(Color.BLUE)

    # If the node is a sensor, display the time taken to reach it
    if node.id().startswith('Sensor '):
        print(f'Reached {node.id()} after {time()-start_time} seconds')

    # For every incident edge
        # If water hasn't flowed through it
            # Calculate how long it will take
            # Set a call to that function after that amount of time

    # For every incident edge
    for edge in node.incident_edges():
        # If water hasn't flowed through it
        if not edge.attribute('flowed'):
            edge.set_attribute('flowed',True)

            # Calculate how long it will take
            wave_time = edge.weight()/edge.attribute('wave_speed')
            wait_time = wave_time*1000*slowmo

            #Traversal animation takes about 500ms
            if wait_time > 500:

                delay(edge.traverse, wait_time-500, args=[node, Color.BLUE, True])
            else:
                edge.traverse(initial_node=node, color=Color.BLUE, keep_path=True)

            # Set a call to that function after that amount of time
            delay(spread, wait_time, args=[edge.other_node(node)])


begin_pynode(run)
