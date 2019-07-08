
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

def main():
    #max_timeslot = input("Type the simulation's number of time_slots")
    #print("Thank you, simulation starting now....")
    loads =  np.linspace(0,1,10, endpoint= False)
    simulation(2, 0.3,10000000)
    # for load in loads:
    #     simulation(load, max_timeslot):


def medium():
    med = {
        "idle":1,
        "nodes":[]
        }
    return med



if __name__ == '__main__':
    main()