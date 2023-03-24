import subprocess
import re

def monitor():
    subprocess.call("ifconfig wlan0 down")
    subprocess.call("iwconfig wlan0 mode monitor")
    subprocess.call("ifconfig wlan0 up")
    print("[+] Changing to monitor mode")

#def check_monitor():
    #find correct regex
    #iwconfig_result = subprocess.check_output("iwconfig wlan0")
    #monitor_result = re.search(r"")

monitor()

    