import lib
from flask import Flask
app = Flask(__name__)
library = lib.get_instance()

import server.routes

def start_server():
	app.debug = True
	app.run(host="0.0.0.0", threaded=True)
