import os
import time
from threading import Thread
from server import variables


def mac_scanner():
    # Get current devices
    result = variables.get('devices', {'devices': []})

    class Device:
        def __init__(self, name='', ip='', mac=''):
            self.name = name
            self.ip = ip
            self.mac = mac
            self.last_seen = time.time()

        def to_dict(self):
            return {'name': self.name,
                    'ip': self.ip,
                    'mac': self.mac,
                    'last_seen': '%d seconds ago' % (time.time() - self.last_seen)}

        def __repr__(self):
            return "{'name': %s, 'ip': %s, 'mac': %s, 'last_seen': '%d seconds ago'}" % \
                   (self.name, self.ip, self.mac, time.time() - self.last_seen)

    def add_device(device):
        # Adds device to list or updates last_seen variable
        for d in result['devices']:
            if d.mac == device.mac:
                # Device already in list, update last_seen variable
                d.last_seen = time.time()
                return
        # Device is new, add to list
        result['devices'].append(device)
        return

    def remove_old_devices():
        for i, d in enumerate(result['devices']):
            if time.time() - d.last_seen > 600:
                # Not seen for 10 minutes, remove device from list
                del result['devices'][i]

    def scan():
        # Call nmap function to scan for connected devices
        response = os.popen("sudo nmap -sn 192.168.1.0/24 | grep 'MAC Address:\|Nmap scan'").read()
        response = response.split('\n')
        result['last_update'] = time.strftime("%Y-%m-%d %H:%M:%S")

        for line in response:
            linesplit = line.split(' ')
            for i, word in enumerate(linesplit):
                if word == 'for':
                    # New device
                    current_device = Device()  # Make new device
                    current_device.name = linesplit[i + 1]  # Name
                    current_device.ip = linesplit[i + 2][1:-1]  # IP
                    break
                if word == 'Address:':
                    current_device.mac = linesplit[i + 1]  # MAC
                    add_device(current_device)  # Add or update device to device list
                    break

        remove_old_devices()  # Remove old devices if not seen for a long time
        variables.put('devices', result, False)  # Update devices variable

    while True:
        scan()
        time.sleep(60)  # Wait one minute before scanning again


def run_services():
    threads = []

    # List all services here
    threads.append(Thread(target=mac_scanner))

    for thread in threads:
        thread.start()


run_services()
