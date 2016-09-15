import sys
import time

def log(string):
    # Flushes stdout after every print to make sure it is in the log file
    print t(), string
    sys.stdout.flush()

def t():
    return "[" + time.strftime('%d/%b/%Y %H:%M:%S') + "]"
