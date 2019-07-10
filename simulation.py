
from Node import Node as Node
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from tabulate import tabulate
import os


def generate_nodes(number_of_nodes, channel, load):
    for i in range(number_of_nodes):
        n = Node(i ,load, channel) 
        channel["nodes"].append(n)
    return channel


def simulation(number_of_nodes, load, max_packets):
    channel = medium()
    done = False
    departed = 0
    network_stats = {}
    final_stats = {}
    network_stats["maximum_delay"] = 0
    network_stats["throughput"] = 0
    network_stats["average_delay"] = 0

    final_stats["maximum_delay"] = 0
    final_stats["throughput"] = 0
    final_stats["average_delay"] = 0
    
    # populate the channel with the nodes instances
    channel = generate_nodes(number_of_nodes, channel, load)
    

    # main simulation loop, each loop is a mini time slot
    # thus time is slotted in mini time slots
    time_slot = 1
    packet_time_slot =  (time_slot / 10)  #packet time slot = time in mini slots that needs a packet to be fully transmitted
    while done == False:
        overall_node_stats = []
        overall_outgoing = []

        for node in channel["nodes"]:
            if time_slot % 10 == 0: #generate a packet every packet_time_slot, i.e every 10 mini_time_slots
                node.packet_generator(time_slot) 
            node_status = node.mac_protocol() #run the protocol for the current node
            node_stats = node.export_stats() #export statistics
            outgoing_queue = node.export_queue()

            overall_node_stats.append(node_stats)
            overall_outgoing.append(outgoing_queue)

            departed = node_stats["departed_packets"] + departed #count all the departed packets from all the nodes
            final_stats["maximum_delay"] = (node_stats["maximum_delay"]/number_of_nodes) + final_stats["maximum_delay"]
            final_stats["average_delay"] = (node_stats["average_delay"]/number_of_nodes) + final_stats["average_delay"]
            final_stats["throughput"] = (node_stats["throughput"]/number_of_nodes) + final_stats["throughput"]

            network_stats["maximum_delay"] = (node_stats["maximum_delay"]/number_of_nodes) + network_stats["maximum_delay"]
            network_stats["average_delay"] = (node_stats["average_delay"]/number_of_nodes) + network_stats["maximum_delay"]
            network_stats["throughput"] = (node_stats["throughput"]/number_of_nodes) + network_stats["maximum_delay"]
        if departed > (1000 * number_of_nodes):
            done = True    
        print_stats(time_slot, network_stats, overall_node_stats, final_stats, done, departed)
        network_stats["maximum_delay"] = 0
        network_stats["throughput"] = 0
        network_stats["average_delay"] = 0
        #I have to zero the counter so it doesn't double add each time_slot.
        departed = 0
        time_slot = time_slot + 1

def print_stats(time_slot, network_stats, overall_node_stats, final_stats, done, departed):
    if time_slot % 10000 == 0:
            os.system('clear')
            print(f"~~~~~~~~`TIME SLOT {time_slot}~~~~~~")
            print (tabulate(overall_node_stats, headers = "keys" ) )
            print(f"\nNumber of packets sent in the network: {departed}")
            print("\nAverage Network-wide statistics\n")
            print( tabulate([network_stats], headers = "keys") )
            a  = input("Press enter to continue") #pause for input so the user has time to examine the statistics
            # print(overall_outgoing)  
    if done == True:
        f_th = final_stats["throughput"] / time_slot
        f_ma = final_stats["maximum_delay"] / time_slot
        f_av = final_stats["average_delay"] / time_slot
        print ("\n Overall network-wide statistics for the entire simulation")
        print(tabulate([final_stats], headers = "keys"))

def main():
    load = 0.4 #load is the propability with wich a new packet will arrive in the outgoing queue
    # of a node at each packet_time_slot (1 packet_time_slot = 10 time slots)
    max_packets = int(input("Type the number of departed packets per node\n"))
    number_of_nodes = int(input("Type the number of simulated nodes that will exist in the channel \n"))
    print("Thank you, simulation starting now....")
    simulation(number_of_nodes, load, max_packets)


def medium():
    med = {
        "idle":1,
        "nodes":[]
        }
    return med



if __name__ == '__main__':
    main()