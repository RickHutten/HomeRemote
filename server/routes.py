import time
import random
import os
import hashlib
import flask
import server.audio
import lib.string
from ast import literal_eval
from flask import abort
from flask import send_file
from flask import request
from flask import render_template
from server import app
from server import library
from server import variables
from lib.log import log

# Set stop_timer on False on server boot
variables.put("stop_timer", False, False)
variables.put("status", variables.STOPPED)


def valid_ip():
    """
    :return: True when the user is permitted to call the function with it's ip,
    False if the user is not permitted.
    """
    ip = request.remote_addr
    return (ip in variables.get("ip", []) or str(request.path) == "/register_ip") and ip not in variables.get("banned",
                                                                                                              [])


def block_user():
    abort(401)


@app.before_request
def limit_remote_address():
    if not valid_ip():
        log("Unauthorised request! -> " + str(request.remote_addr))
        abort(401)  # Unauthorized


@app.route("/")
def show_homepage():
    return render_template("home.html"), 200


@app.route("/register_ip")
def register_ip():
    ip = request.remote_addr
    key = request.args.get("key")
    if key is None:
        log("Registery denied")
        return "Register failed"
    if hashlib.sha224(key).hexdigest() != \
            "e40206e07b61b34c898d38e6756d99c6bbc74279445afa320c0eb053":
        bannedlist = variables.get("banned", [])
        bannedlist.append(ip)
        variables.put("banned", bannedlist)
        log("IP banned")
        return "IP banned"
    ips = variables.get("ip", [])
    if ip in ips:
        log("IP already registered")
        return "IP already registered"
    ips.append(ip)
    variables.put("ip", ips)
    log("Registered succesfully")
    return "Registered succesfully"


@app.route("/print_lib_short")
def print_library_short():
    library.print_lib_short()
    return "Library printed in terminal"


@app.route("/print_lib")
def print_library():
    library.print_lib()
    return "Library printed in terminal"


@app.route("/poll")
def long_poll():
    status = variables.get("status", "STOPPED")
    artist, album, song = variables.get("playing", [])
    while True:
        # Return when the song has changed
        new_status = variables.get("status", "STOPPED")
        new_artist, new_album, new_song = variables.get("playing", [])
        if artist != new_artist or album != new_album or song != new_song or status != new_status:
            # New song is played
            return get_status()
        time.sleep(0.5)


@app.route("/play", methods=['POST'])
def play_music():
    """
    Play the song requested by POST request
    :return: Json of song information
    """
    if not valid_ip():
        block_user()

    data = request.data
    data = literal_eval(data)

    artist = lib.string.cleanJSON(data["artist"])
    album = lib.string.cleanJSON(data["album"])
    song = lib.string.cleanJSON(data["song"])

    songObj = library.get_song(artist, album, song)
    server.audio.play(songObj)
    return get_status()


@app.route("/play/<string:artist>")
def play_music_artist(artist):
    """
    Shuffle the artist.
    :param artist: String of artist name
    :return: Not important
    """
    artist = artist.replace("_", " ").replace("&amp;", "&")
    artist_object = library.get_artist(artist)
    songs = artist_object.get_songs()
    random.shuffle(songs)

    # Set playlist
    playlist = []
    for song in songs:
        artist_name = song.get_artist().get_name()
        album_title = song.get_album().get_title()
        song_name = song.get_title()
        playlist.append([artist_name, album_title, song_name])
    # TODO: push queue to user
    variables.put("queue", playlist)

    # Play first song
    song = songs[0]
    server.audio.play(song)
    return "Playing %s by %s : %s" % (song.get_title(),
                                      song.get_artist().get_name(),
                                      song.get_album().get_title())


@app.route("/play/<string:artist>/<string:album>")
def play_music_album(artist, album):
    """
    Shuffle the album.
    :param artist: String of artist name
    :param album: String of album name
    :return: Not important
    """
    artist = artist.replace("_", " ").replace("&amp;", "&")
    album = album.replace("_", " ").replace("&amp;", "&")

    album_object = library.get_album(artist, album)
    songs = album_object.get_songs()
    random.shuffle(songs)

    # Set playlist
    playlist = []
    for song in songs:
        artist_name = song.get_artist().get_name()
        album_title = song.get_album().get_title()
        song_name = song.get_title()
        playlist.append([artist_name, album_title, song_name])

    variables.put("queue", playlist)

    # Play first song
    song = songs[0]
    server.audio.play(song)
    return "Playing %s by %s : %s" % (song.get_title(),
                                      song.get_artist().get_name(),
                                      song.get_album().get_title())


@app.route("/play/<string:artist>/<string:album>/<string:song>")
def play_music_song(artist, album, song):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    album = album.replace("_", " ").replace("&amp;", "&")
    song_name = song.replace("_", " ").replace("&amp;", "&")

    song = library.get_song(artist, album, song_name)
    server.audio.play(song)
    return "Playing %s by %s : %s" % (song.get_title(),
                                      song.get_artist().get_name(),
                                      song.get_album().get_title())


@app.route("/stop")
def stop_music():
    server.audio.stop()
    return "Music was stopped"


@app.route("/pause")
def pause_music():
    server.audio.pause()
    song = server.audio.get_playing()
    if song is None:
        return "Can't pause. Nothing is playing"
    return "Music paused: %s by %s : %s" % (song.get_title(),
                                            song.get_artist().get_name(),
                                            song.get_album().get_title())


@app.route("/resume")
def resume_music():
    server.audio.resume()
    song = server.audio.get_playing()
    if song is None:
        return "Can't resume. Nothing is playing"
    return "Resumed playing %s by %s : %s" % (song.get_title(),
                                              song.get_artist().get_name(),
                                              song.get_album().get_title())


@app.route("/next")
def next_song():
    queue = variables.get("queue", None)
    playing = variables.get("playing", None)
    if queue is None or playing is None:
        return "Something went wrong"
    queue_nr = queue.index(playing)
    song = queue[(queue_nr + 1) % len(queue)]
    song_obj = library.get_song(song[0], song[1], song[2])
    server.audio.play(song_obj)
    return song[0] + ";" + song[1] + ";" + song[2]


@app.route("/previous")
def previous_song():
    queue = variables.get("queue", None)
    playing = variables.get("playing", None)
    if queue is None or playing is None:
        return "Something went wrong"
    queue_nr = queue.index(playing)
    if variables.get("elapsed", 0) > 4:
        # Replay the song
        song = playing
        log("Replaying song from beginning:" + str(song))
    else:
        # Play the previous song
        song = queue[queue_nr - 1]
    song_obj = library.get_song(song[0], song[1], song[2])
    server.audio.play(song_obj)

    return song[0] + ";" + song[1] + ";" + song[2]


@app.route("/image", methods=['POST'])
def get_image():
    """
    Get the image of the requested artist or album
    Json argument 'album' is optional, when not given the 
    image of the artist is returned
    """
    if not valid_ip():
        block_user()

    data = request.data
    data = literal_eval(data)

    artist = lib.string.cleanJSON(data["artist"])

    if "album" not in data.keys():
        # No album is given, return the artist image
        try:
            filename = library.get_artist(artist).get_image()
        except StandardError:
            # The image is not found
            return abort(404)
        return send_file(filename, mimetype="image/jpg")

    # Album is given, return album image
    album = lib.string.cleanJSON(data["album"])
    try:
        filename = library.get_album(artist, album).get_image()
    except StandardError:
        # The image is not found
        return abort(404)
    return send_file(filename, mimetype="image/jpg")


@app.route("/image/<string:artist>/<string:album>")
def get_album_image(artist, album):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    album = album.replace("_", " ").replace("&amp;", "&")
    try:
        filename = library.get_album(artist, album).get_image()
    except StandardError:
        # The image is not found
        return abort(404)
    return send_file(filename, mimetype="image/jpg")


@app.route("/image/<string:artist>")
def get_artist_image(artist):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    try:
        filename = library.get_artist(artist).get_image()
    except StandardError:
        # The image is not found
        return abort(404)
    return send_file(filename, mimetype="image/jpg")


@app.route("/shutdown")
def shutdown():
    log("Shutting down server...")
    # Fade audio out
    server.audio.fade_out(1)
    os.system("sudo shutdown -h now")
    return "Shutting down server..."


# Niet meer nodig bij JSON
@app.route("/artists")
def get_artists():
    s = ""
    for artist in library.get_artists():
        s += artist.get_name() + ";"
    return s[:-1]


@app.route("/artists2")
def get_artists2():
    artistlist = []
    for artist in sorted(library.get_artists(), key=lambda a: a.get_name()):
        jobject = {"name": artist.get_name(),
                   "albums": len(artist.get_albums()),
                   "songs": len(artist.get_songs())}
        artistlist.append(jobject)

    json = {"artists": artistlist}
    return flask.jsonify(**json)


# Niet meer nodig bij JSON
@app.route("/albums")
def get_albums():
    s = ""
    for album in library.get_albums():
        s += album.get_title() + ":" + album.get_artist().get_name() + ";"
    return s[:-1]


@app.route("/albums2")
def get_albums2():
    albumlist = []
    for album in sorted(library.get_albums(), key=lambda a: a.get_title()):
        jobject = {"title": album.get_title(),
                   "artist": album.get_artist().get_name(),
                   "songs": len(album.get_songs())}
        albumlist.append(jobject)

    json = {"albums": albumlist}
    return flask.jsonify(**json)


# Niet meer nodig bij JSON
@app.route("/get/<string:artist>")
def get_albums_of_artist(artist):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    artist_object = library.get_artist(artist)
    s = ""
    for album in artist_object.get_albums():
        s += album.get_title() + ";"
    return s[:-1]


@app.route("/get2/<string:artist>")
def get2_albums_of_artist(artist):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    artist_object = library.get_artist(artist)
    albums = artist_object.get_albums()
    album_list = []
    for album in albums:
        song_list = []
        for song in sorted(album.get_songs(), key=lambda a: a.get_order()):
            song_list.append({"title": song.get_title(),
                              "artist": song.get_artist().get_name(),
                              "order": song.get_order(),
                              "duration": song.get_duration()})
        album_list.append({"title": album.get_title(),
                           "songs": song_list})
    json = {"albums": album_list}
    return flask.jsonify(**json)


@app.route("/get2/<string:artist>/<string:album>")
def get2_albums(artist, album):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    album = album.replace("_", " ").replace("&amp;", "&")
    album = library.get_album(artist, album)
    song_list = []
    for song in sorted(album.get_songs(), key=lambda a: a.get_order()):
        song_list.append({"title": song.get_title(),
                          "artist": song.get_artist().get_name(),
                          "order": song.get_order(),
                          "duration": song.get_duration()})

    json = {"title": album.get_title(),
            "albumartist": album.get_artist().get_name(),
            "songs": song_list}
    return flask.jsonify(**json)


# Niet meer nodig bij JSON
@app.route("/get/<string:artist>/<string:album>")
def get_songs_of_album(artist, album):
    artist = artist.replace("_", " ").replace("&amp;", "&")
    album = album.replace("_", " ").replace("&amp;", "&")
    album_object = library.get_album(artist, album)
    s = ""
    for song in sorted(album_object.get_songs(), key=lambda a: a.get_order()):
        s += song.get_title() + ":" + str(song.get_duration()) + ";"
    return s[:-1]


# Should not be used any more, doesn't use JSON
@app.route('/set/queue', methods=['POST'])
def post_queue():
    if not valid_ip():
        block_user()
    data = request.data
    song_strings = data.split(";")
    playlist = []
    for song_str in song_strings:
        artist_name, album_title, song_name = song_str.split(":")
        playlist.append([artist_name, album_title, song_name])
    variables.put("queue", playlist)
    return get_status()


@app.route('/set2/queue', methods=['POST'])
def post_queue2():
    """
    Data: {"songs": [ {"artist": artist, "album": album, "song": song}, ...]}
    """
    if not valid_ip():
        block_user()
    data = request.data
    print [data]
    print ""
    data = literal_eval(data)
    print [data]

    songs = data["songs"]
    playlist = []
    print "hier"

    for song in songs:
        artist = lib.string.cleanJSON(song["artist"])
        album = lib.string.cleanJSON(song["album"])
        song_name = lib.string.cleanJSON(song["song"])
        print artist, album, song_name

        playlist.append([artist, album, song_name])

    variables.put("queue", playlist)
    return get_status()


@app.route("/queue")
def get_queue():
    queue = variables.get("queue", [])
    if not queue:  # Queue is empty
        return "No queue found"
    songlist = []
    for song in queue:
        songObj = library.get_song(song[0], song[1], song[2])
        songlist.append({"artist": song[0], "album": song[1], "song": song[2], "duration": songObj.get_duration()})
    json = {"queue": songlist}
    return flask.jsonify(**json)


@app.route("/set/volume/<int:volume>")
def set_music_volume(volume):
    if server.audio.set_volume(volume):
        return "Volume set to " + str(volume) + "%"
    return "Can not set volume to " + str(volume) + "%"


@app.route("/get_local_devices")
def get_local_devices():
    # Return the devices connected to the local network of the server
    json = variables.get("devices", {'devices': []})
    for i, d in enumerate(json['devices']):
        json['devices'][i] = d.to_dict()
    return flask.jsonify(**json)


@app.route("/status")
def get_status():
    # Returns JSON with server status
    artist, album, song = variables.get("playing", [])
    json = dict()
    status = variables.get("status", -1)
    json["status"] = status

    elapsed = int(time.time() - variables.get("started_on", 0))
    json["uptime"] = "%dh %dm %ds" % (elapsed/3600, elapsed/60 % 60, elapsed % 60)

    if status != variables.STOPPED:
        json["playing"] = {"artist": artist, "album": album, "song": song,
                           "elapsed": variables.get("elapsed", 0),
                           "duration": variables.get("song_duration", 0)}
    json["volume"] = variables.get("volume", 50)
    return flask.jsonify(**json)


@app.route("/push")
def push():
    server.audio.push()
    return "User notified"


@app.route("/register_token", methods=['POST'])
def register_token():
    if not valid_ip():
        block_user()
    data = request.data
    log("Token: " + str(data))
    tokens = variables.get("gmc_tokens", [])
    if data not in tokens:
        tokens.append(data)
        variables.put("gcm_tokens", tokens)
    return "Successfully registered token: %s" % data
