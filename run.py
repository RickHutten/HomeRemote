#!/usr/bin/env python
import server
import warnings
import argparse
from lib.log import log

# Get rid of those f*cking warnings of Flask
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log", help="Logs the output to a log file.", action="store_true")

args = parser.parse_args()

if args.log:
    import sys
    import time
    sys.stderr = open("./log/%s.txt" %(time.strftime('%d-%m-%y %H:%M:%S')), "w")
    sys.stdout = sys.stderr

log("Starting server")

server.start_server()
