import lib
import lib.variables
from flask import Flask

app = Flask(__name__)
library = lib.get_instance()  # Get the music library
variables = lib.variables.ServerVariables()  # Import server variables instance

import server.routes  # Has to be imported after declaring variables 'app', 'library' and 'variables'

def start_server():
	app.debug = True
	app.run(host="0.0.0.0", threaded=True)
