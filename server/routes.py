import time
import random
import os
import flask
import lib.variables
from flask import abort, send_file
from server import app, library

# Make variables
variables = lib.variables.ServerVariables()

def play(song):
	variables.put("playing", [song.get_title(), song.get_artist().get_name(), song.get_album().get_title()])
	os.system("pkill mpg123")  # Kill everything that might be playing
	os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
	print t(), "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

def get_playing():
	# Return songObject of song played	
	ans = variables.get("playing")
	if ans == None:
		return ans
	song, artist, album = ans
	albumObject = library.get_album(artist, album)
	return albumObject.get_song(song)

def pause():
	os.system("pkill -STOP mpg123")

def resume():
	os.system("pkill -CONT mpg123")

def stop():
	variables.put("playing", None)
	os.system("pkill mpg123")
		

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
	play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

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
	play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/play/<string:artist>/<string:album>")
def play_music_album(artist, album):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")

	albumObject = library.get_album(artist, album)
	songs = albumObject.get_songs()
	random.shuffle(songs)
	song = songs[0]
	play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/play/<string:artist>/<string:album>/<string:song>")
def play_music_song(artist, album, song):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")
	song = song.replace("_", " ")

	albumObject = library.get_album(artist, album)
	song = albumObject.get_song(song)
	
	play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/stop")
def stop_music():
	stop()
	return "Music was stopped"

@app.route("/pause")
def pause_music():
	pause()
	song = get_playing()
	if song == None:
		return "Can't pause. Nothing is playing"
	return "Music paused: %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/resume")
def resume_music():
	resume()
	song = get_playing()
	if song == None:
		return "Can't resume. Nothing is playing"
	return "Resumed playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title()) 

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

@app.route("/artists")
def get_artists():
	s = ""
	for artist in library.get_artists():
		s += artist.get_name() + ";"
	return s[:-1]

@app.route("/albums")
def get_albums():
	s = ""
	for album in library.get_albums():
		s += album.get_title() + ":" + album.get_artist().get_name() + ";"
	return s[:-1]

@app.route("/<string:artist>")
def get_albums_of_artist(artist):
	artist = artist.replace("_", " ")
	artistObject = library.get_artist(artist)
	s = ""
	for album in artistObject.get_albums():
		s += album.get_title() + ";"
	return s[:-1]

@app.route("/<string:artist>/<string:album>")
def get_songs_of_album(artist, album):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")
	albumObject = library.get_album(artist, album)
	s = ""
	for song in albumObject.get_songs():
		s += song.get_title() + ";"
	return s[:-1]

@app.route("/playing")
def get_playing_song():
	song = get_playing()
	if song == None:
		return "Nothing is playing"
	return "Currently playing: %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())
