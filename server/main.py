import lib.main
import time
import random
import os
import flask
from flask import Flask, abort, send_file 

app = Flask(__name__)


library = lib.main.get_instance()

def t():
	return "[" + time.asctime( time.localtime(time.time()) ) + "]"

@app.route("/")
def home():
	print t(), "Jaap is faggot"
	return "Jaap is fag"

@app.route("/print_lib")
def print_liberary():
	library.print_lib_short()
	return "Library printed in terminal"

@app.route("/play")
def play_music():
	songs = library.get_songs()
	random.shuffle(songs)
	song = songs[0]
	os.system("pkill mpg123")  # Kill everything that might be playing
	os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
	print t(), "Playing %s by %s" % (song.get_title(), song.get_artist().get_name())
	return "Playing %s by %s" % (song.get_title(), song.get_artist().get_name()) # Show the user what song is playing

@app.route("/stop")
def stop_music():
	os.system("pkill mpg123")
	return "Music was stopped"

@app.route("/image/<string:artist>/<string:album>")
def get_image(artist, album):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")
	print t(), "Requesting image for", artist, ":" ,album
	try:
		filename = library.get_album(artist, album).get_image()
	except StandardError:
		# The image is not found
		return abort(404)
	return send_file(filename, mimetype="image/jpg")
	
def start_server():
	app.debug = True
	app.run(host="0.0.0.0", threaded=True)


