import subprocess
import optparse 
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for changing Mac Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify interface, use --help for more information")
    elif not options.new_mac:
        parser.error("[-] Please specify interface, use --help for more information")        
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] Changing mac address for" + interface + "to" + new_mac)

def check_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_changer_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    print(mac_changer_result)
    if mac_changer_result:
        return mac_changer_result(0)
    else:
        print("[-] Couldn't read MAC address")

options = get_arguments()

current_mac = check_mac(options.interface)
print("Current MAC ="+ str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = check_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address has changed successfully to" + current_mac)
else:
    print("[-] Mac address didn't change")



