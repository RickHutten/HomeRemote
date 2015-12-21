import time
import random
import os
import flask
from flask import abort, send_file
from server import app, library

def t():
	return "[" + time.asctime( time.localtime(time.time()) ) + "]"

@app.route("/print_lib_short")
def print_liberary_short():
	library.print_lib_short()
	return "Library printed in terminal"

@app.route("/print_lib")
def print_liberary():
	library.print_lib()
	return "Library printed in terminal"

@app.route("/play")
def play_music():
	songs = library.get_songs()
	random.shuffle(songs)
	song = songs[0]
	os.system("pkill mpg123")  # Kill everything that might be playing
	os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
	print t(), "Playing %s by %s" % (song.get_title(), song.get_artist().get_name())
	return "Playing %s by %s" % (song.get_title(), song.get_artist().get_name())

@app.route("/play/<string:artist>")
def play_music_artist(artist):
	artist = artist.replace("_", " ")
	artistObject = library.get_artist(artist)
	albums = artistObject.get_albums()
	songs = []
	for album in albums:
		for song in album.get_songs():
			songs.append(song)
	random.shuffle(songs)
	song = songs[0]
	os.system("pkill mpg123")  # Kill everything that might be playing
	os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
	print t(), "Playing %s by %s" % (song.get_title(), song.get_artist().get_name())
	return "Playing %s by %s" % (song.get_title(), song.get_artist().get_name())

@app.route("/stop")
def stop_music():
	os.system("pkill mpg123")
	return "Music was stopped"

@app.route("/pause")
def pause_music():
	os.system("pkill -STOP mpg123")
	song = song_played
	if song == None:
		return "Can't pause. Nothing is playing"
	return "Music paused: %s by %s" % (song.get_title(), song.get_artist().get_name())

@app.route("/resume")
def resume_music():
	os.system("pkill -CONT mpg123")
	song = song_played
	if song == None:
		return "Can't pause. Nothing is playing"
	return "Resumed playing %s by %s" % (song.get_title(), song.get_artist().get_name()) 

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

@app.route("/shutdown")
def shutdown():
	os.system("sudo shutdown now")
	return "Shutting down server..."
