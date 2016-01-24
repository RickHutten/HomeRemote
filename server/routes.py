import time
import random
import os
import hashlib
import flask
import server.audio
from flask import abort, send_file, request
from server import app, library, variables

# Set stop_timer on False on server boot
variables.put("stop_timer", False)

def t():
	return "[" + time.asctime( time.localtime(time.time()) ) + "]"

@app.before_request
def limit_remote_addr():
	ip = request.remote_addr
	if ip not in variables.get("ip", []) and str(request.path) != "/register_ip":
		print t(), "Unauthorised request! ->", request.remote_addr
		abort(401)  # Unauthorized
	if ip in variables.get("banned", []):
		print t(), "Banned IP acces denied"
		abort(403)  # Forbidden

@app.route("/register_ip")
def register_ip():
	ip = request.remote_addr
	print "\n", t(), "IP registery attempt! ->", ip, "  ", 
	key = request.args.get("key")
	if key == None:
		print "Registery denied\n"
		return "Register failed"
        if hashlib.sha224(key).hexdigest() != "e40206e07b61b34c898d38e6756d99c6bbc74279445afa320c0eb053":
		bannedlist = variables.get("banned", [])
		bannedlist.append(ip)
		variables.put("banned", bannedlist)
		print "IP banned\n"
		return "IP banned" 
	ips = variables.get("ip", [])
	if ip in ips:
		print "IP already registered\n"
		return "IP already registered"
	ips.append(ip)
	variables.put("ip", ips)
	print "Registered succesfully\n"
	return "Registered succesfully"
	
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
	server.audio.play(song)
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
	server.audio.play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/play/<string:artist>/<string:album>")
def play_music_album(artist, album):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")

	albumObject = library.get_album(artist, album)
	songs = albumObject.get_songs()
	random.shuffle(songs)
	song = songs[0]
	server.audio.play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/play/<string:artist>/<string:album>/<string:song>")
def play_music_song(artist, album, song):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")
	song = song.replace("_", " ")

	albumObject = library.get_album(artist, album)
	song = albumObject.get_song(song)

	server.audio.play(song)
	return "Playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/stop")
def stop_music():
	server.audio.stop()
	return "Music was stopped"

@app.route("/pause")
def pause_music():
	server.audio.pause()
	song = server.audio.get_playing()
	if song == None:
		return "Can't pause. Nothing is playing"
	return "Music paused: %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title())

@app.route("/resume")
def resume_music():
	server.audio.resume()
	song = server.audio.get_playing()
	if song == None:
		return "Can't resume. Nothing is playing"
	return "Resumed playing %s by %s : %s" % (song.get_title(), song.get_artist().get_name(), song.get_album().get_title()) 

@app.route("/next")
def next_song():
	queue = variables.get("queue", None)
	playing = variables.get("playing", None)
	if queue == None or playing == None:
		return "Something went wrong"
	queue_nr = queue.index(playing)
	song = queue[(queue_nr + 1)%len(queue)]
	songObj = library.get_song(song[0], song[1], song[2])
	server.audio.play(songObj)
	print "Playing next song:", song
	return song[0] + ";" + song[1] + ";"+ song[2]

@app.route("/previous")
def previous_song():
	queue = variables.get("queue", None)
	playing = variables.get("playing", None)
	if queue == None or playing == None:
		return "Something went wrong"
	queue_nr = queue.index(playing)
	song = queue[queue_nr - 1]
	songObj = library.get_song(song[0], song[1], song[2])
	server.audio.play(songObj)
	print "Playing previous song:", song
	return song[0] + ";" + song[1] + ";"+ song[2]

@app.route("/image/<string:artist>/<string:album>")
def get_image(artist, album):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")
	try:
		filename = library.get_album(artist, album).get_image()
	except StandardError:
		# The image is not found
		return abort(404)
	return send_file(filename, mimetype="image/jpg")

@app.route("/shutdown")
def shutdown():
	os.system("sudo shutdown -h now")
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

@app.route("/get/<string:artist>")
def get_albums_of_artist(artist):
	artist = artist.replace("_", " ")
	artistObject = library.get_artist(artist)
	s = ""
	for album in artistObject.get_albums():
		s += album.get_title() + ";"
	return s[:-1]

@app.route("/get/<string:artist>/<string:album>")
def get_songs_of_album(artist, album):
	artist = artist.replace("_", " ")
	album = album.replace("_", " ")
	albumObject = library.get_album(artist, album)
	s = ""
	for song in sorted(albumObject.get_songs(), key=lambda a: a.get_order()):
		s += song.get_title() + ":" + song.get_duration() + ";"
	return s[:-1]

@app.route('/set/queue', methods=['POST'])
def post_queue():
	limit_remote_addr()  # Limit
	data = [request.data][0]
	song_strings = data.split(";")
	playlist = []
	for song_str in song_strings:
		artist_name, album_title, song_name = song_str.split(":")
		songObj = library.get_song(artist_name, album_title, song_name)
		playlist.append([artist_name, album_title, song_name])
	variables.put("queue", playlist)
	return "Queue received succesfully"

@app.route("/queue")
def get_route():
	queue = variables.get("queue", [])
	if queue == []:
		return " "
	result = ""
	for item in queue:
		artist, album, song = item
		result += artist + ":" + album + ":" + song + ";"	
	return result[:-1]
	
@app.route("/set/volume/<string:volume>")
def set_music_volume(volume):
	if server.audio.set_volume(int(volume)):
		return "Volume set to " + volume + "%"
	return "Can not set volume to " +  volume + "%"

@app.route("/playing")
def get_playing_song():
	song = server.audio.get_playing()
	if song == None:
		return "Nothing is playing"
	return "%s - %s" % (song.get_title(), song.get_artist().get_name())

