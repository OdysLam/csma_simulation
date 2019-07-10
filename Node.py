
from random import randint, choice


class Node:
    def __init__(self, node_id, load, medium):
        #node specific
        # In this simulation, we use 2 distinct time_slots. The CSMA mini time slot which is used as time_slots
        # and the packet_time_slot which is the number of mini_time_slots that are needed for a packet to be fully transmitted.
        # In this simulation, we let that packet_time_slot = 10 time slots. The unit of time is a packet_time_slot.
        self.incoming = []
        self.outgoing = []
        self.backoff_counter = 0
        self.node_id = node_id
        self.collision = False
        self.load = load
        self.medium = medium # medium is dictionary {"idle":1, "nodes":[node1, node2,]}
                               #they are in the same list, thus neighbours

        #stats
        self.average_delay = 0
        self.sum_delay = 0
        self.max_delay = 0 
        self.throughput = 0
        self.delays = []
        self.departed_packet_counter = 0
        self.packets_dropped = 0
        self.send_attempt = 0
        self.total_load = 0

        #csma specific
        self.transmitting = False
        self.wait_time_slot = True
        self.transmit = False

    def mac_protocol(self):
        self.collision = False # node no longer needs the collision flag enabled
        if self.backoff_counter > 0:
            self.backoff_counter = self.backoff_counter - 1
            return f"back off mode, {self.backoff_counter} time_slots remaining"
        if self.transmit == False:
            if self.medium_idle():
                if self.outgoing: #check if there is something to transmit
                    self.transmit = True #wait one idle time_slot before sending
                    return "transmission starts at next time_slot"
            elif self.medium_idle() == False:
                return "Medium is busy, Node innactive"
        #if I have transmit, i don't care about the status of the medium, the node
        # will transmit at the next time_slot with propability 1
        elif self.transmit == True: 
            self.detect_collision()
            if self.collision == True:
                self.backoff_counter = randint(0,25)
                self.transmit = False #reset algorithm
                self.medium["idle"] = True
                return "backoff activated"
            #transmit normally
            self.medium["idle"] = False
            self.send_frame()
            return "node_active"

    def detect_collision(self):
        for node in self.medium["nodes"]:
            if  node.node_id != self.node_id: 
                if (node.transmit == True or node.collision == True):
                    self.collision = True 
                    #if a node has begin_tranmission flag as true, activated during the previews time_slot
                    # it is certain that in this time_slot it will transmit,thus we will have a           
                    return True
        return False 
        
    def medium_idle(self):
        return self.medium["idle"] #True or False

    def send_frame(self): #take first packet in the queue    
        self.outgoing[0]["packet_size"] = self.outgoing[0]["packet_size"] - 1
        self.send_attempt = self.send_attempt + 1
        frames_left = self.outgoing[0]["packet_size"]
        delay = 0
        if frames_left == 0:
            packet_left = self.outgoing.pop(0) # packet succesfully transmitted in this time_slot
            self.departed_packet_counter = self.departed_packet_counter + 1
            delay = (self.time_slot - packet_left["generated_time_slot"]) / 10 #we count in packet_time_slots
            self.transmit = False #The node no longer transmits
            self.medium["idle"] = True #the medium is idle (from the part of the Node)
        self.update_stats(delay)
    
    def update_stats(self, delay):
        #stats are counted in packet_time_slots
        if delay > self.max_delay:
            self.max_delay = delay
        self.sum_delay = delay + self.sum_delay
        try:
            self.average_delay = self.sum_delay / self.departed_packet_counter
        except ZeroDivisionError:
            self.average_delay = 0
        self.throughput = self.departed_packet_counter / (self.time_slot / 10)
        self.total_load = self.send_attempt / (self.time_slot / 10)

    def export_stats(self):
        return {
            "node_id":self.node_id,
            "average_delay":self.average_delay,
            "overall_delay":self.sum_delay,
            "maximum_delay":self.max_delay,
            "departed_packets":self.departed_packet_counter,
            "throughput":self.throughput,
            "total_load":self.total_load,

        }
    def export_queue(self):
        return self.outgoing

    def packet_generator(self, time_slot):
        load = self.load * 10
        self.time_slot = time_slot
        self.neighbour_count = len(self.medium["nodes"])
        r = randint(1,10)
        if r >= load:
            if len(self.outgoing) == 10:
                self.packets_dropped = self.packets_dropped + 1
                return "packet dropped"
            target_index = list(range(self.neighbour_count))
            target_index.remove(self.node_id)
            target_index = choice(target_index)
            target = self.medium["nodes"][target_index].node_id
    #       packet = [source, target, time_slot_generated]
            packet_size = 10 #in time_slots needed to be transmitted, 1 frame = 1 time_slot
            packet = {
                    "source_node":self.node_id, 
                    "target_node": target, #needless as all nodes transmit over same medium (like ethernet)
                    "packet_size": packet_size, 
                    "generated_time_slot": self.time_slot
                    }
            self.outgoing.append(packet)

