# def create_graph_table(medium,max_time_slots):
#     nodes = medium["nodes"]
#     plt.ion()
#     fig = plt.figure()
#     fig.subplots_adjust(hspace=0.4, wspace=0.4)
#     time_slots = np.linspace(0,max_time_slots,1)
#     subplots = {}
#     for node in nodes:
#         node_id = node.node_id
#         graph_name = f"NODE: {node_id + 1 }"
#         ax = fig.add_subplot(2, 5, node_id+ 1)
#         ax.text( 0.5, 0.5, graph_name, fontsize=18, ha='center')        
#         subplots[node_id] = ax

#     return subplots

# def update_graph_table(overall_node_stats, subplots):

#     for node in overall_node_stats:
#         y_max = node["maximum_delay"]
#         y_av = node["average_delay"]
#         y_th = node["throughput"]
#         max_delay = ax.plot(time_slots,y_max,'-o',alpha=0.8)
#         average_delay = ax.plot(time_slots,y_av,'-o',alpha=0.8)
#         throughput = ax.plot(time_slots,y_th,'-o',alpha=0.8)
    
#     graph_data = open('example.txt','r').read()
#     lines = graph_data.split('\n')
#     xs = []
#     ys = []
#     for line in lines:
#         if len(line) > 1:
#             x, y = line.split(',')
#             xs.append(float(x))
#             ys.append(float(y))
#     ax1.clear()
#     ax1.plot(xs, ys)