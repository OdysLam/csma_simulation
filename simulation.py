
from Node import Node as Node
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from tabulate import tabulate
import os


def simulation(number_of_nodes, load, max_timeslot):
    channel = medium()
    for i in range(number_of_nodes):
        n = Node(i ,load, channel)
        channel["nodes"].append(n)
    subplots = create_graph_table(channel,max_timeslot)
    time_slot = 1
    while time_slot < max_timeslot:
        overall_node_stats = []
        overall_outgoing = []
        if time_slot % 10000 ==0:
            os.system('clear')
        for node in channel["nodes"]:
            node.packet_generator(time_slot)
            node_status = node.mac_protocol()

            node_stats = node.export_stats()
            outgoing_queue = node.export_queue()

            overall_node_stats.append(node_stats)
            overall_outgoing.append(outgoing_queue)
            # if time_slot % 10000 == 0:
            #     print (f"Node: {node.node_id}, Status: {node_status}")
            #     try:
            #         packet = outgoing_queue[0]
            #     except:
            #         packet = []
            #     print(packet)
        if time_slot % 10000 == 0:
            print(f"~~~~~~~~`TIME SLOT {time_slot}~~~~~~")
            print (tabulate(overall_node_stats, headers = "keys" ) )
            # print(overall_outgoing)
        time_slot = time_slot + 1
        update_graph_table(overall_node_stats,subplots )

def main():
    #max_timeslot = input("Type the simulation's number of time_slots")
    #print("Thank you, simulation starting now....")
    loads =  np.linspace(0,1,10, endpoint= False)
    simulation(2, 0.3,10000000)
    # for load in loads:
    #     simulation(load, max_timeslot):


def create_graph_table(medium,max_time_slots):
    nodes = medium["nodes"]
    plt.ion()
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    time_slots = np.linspace(0,time_slots,1)
    subplots = {}
    for node in nodes:
        node_id = node.node_id
        graph_name = f"NODE: {node_id + 1 }"
        ax = fig.add_subplot(2, 5, node_id+ 1)
        ax.text( 0.5, 0.5, graph_name, fontsize=18, ha='center')        
        subplots[node_id] = ax

    return subplots

def update_graph_table(overall_node_stats, subplots):

    for node in overall_node_stats:
        y_max = node["maximum_delay"]
        y_av = node["average_delay"]
        y_th = node["throughput"]
        max_delay = ax.plot(time_slots,y_max,'-o',alpha=0.8)
        average_delay = ax.plot(time_slots,y_av,'-o',alpha=0.8)
        throughput = ax.plot(time_slots,y_th,'-o',alpha=0.8)
    
    graph_data = open('example.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)


def medium():
    med = {
        "idle":1,
        "nodes":[]
        }
    return med



if __name__ == '__main__':
    main()