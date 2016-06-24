import lib
from server.variables import ServerVariables
from flask import Flask

app = Flask(__name__)
library = lib.get_instance()  # Get the music library
variables = ServerVariables()  # Import server variables instance

# Has to be imported after declaring variables 'app', 'library' and 'variables'
import server.routes


def start_server():
    app.debug = False
    app.run(host="0.0.0.0", port=80, threaded=True)
