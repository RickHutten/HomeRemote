import os
import time
from threading import Thread
from server import variables


def mac_scanner():
    response = os.popen("sudo nmap -sn 192.168.1.0/24 | grep 'MAC Address:\|Nmap scan'").read()
    response = response.split('\n')
    result = []
    for line in response:
        linesplit = line.split(' ')
        for i, word in enumerate(linesplit):
            if word == 'for':
                result.append([linesplit[i + 1]])
                break
            if word == 'Address:':
                result[-1].append(linesplit[i + 1])
                break
    result = [i for i in result if len(i) == 2]  # Remove items where no MAC is set
    variables.put('devices', result, False)
    time.sleep(60)  # Wait two minutes before calling itself again
    mac_scanner()  # Scan again


def run_services():
    threads = []

    # List all services here
    threads.append(Thread(target=mac_scanner))

    for thread in threads:
        thread.start()


run_services()
