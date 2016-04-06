#!/usr/bin/env python
import server
import warnings

# Get rid of those f*cking warnings of Flask
warnings.filterwarnings("ignore")

server.start_server()
