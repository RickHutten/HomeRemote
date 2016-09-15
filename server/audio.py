import time
import os
from threading import Thread
from server import library
from server import variables
from server import app
from flask_pushjack import FlaskGCM
from lib.log import log


def play(song):
    log("Playing song: %s by %s" %(song.get_title(), song.get_artist().get_name()))
    variables.put("status", variables.PLAYING)
    variables.put("playing",
                  [song.get_artist().get_name(), song.get_album().get_title(),
                   song.get_title()])
    variables.put("song_duration", song.get_duration())
    variables.put("song_start", time.time(), False)
    os.system("pkill mpg123")  # Kill everything that might be playing
    os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
    push()  # Notify the users

    # Start counting in new thread
    thread = Thread(target=start_timer)
    thread.start()


def set_volume(vol, fade=False):
    # Set volume in percentage. Volume has to be between 0 and 100
    if 0 <= vol <= 100:
        # Don't set new volume if this function is called for fading in or out
        if not fade:
            variables.put("volume", vol)
        if vol == 0:
            os.system("amixer -q sset PCM 0%")
            return True
        # Map 0-100% to 50-100% through a function
        percentage = 5 * vol**0.5 + 50
        command = "amixer -q sset PCM " + str(percentage) + "%"
        os.system(command)
        return True
    return False


def fade_out(s):
    # Music paused afterwards and original volume restored.
    if s < 0.5:
        log("Time to fade out may not be smaller than 0.5 seconds.")
        s = 0.5
    volume = variables.get("volume", 75)
    s -= 0.5  # Compensate for computing time
    for i in range(20):
        vol = volume * (1 - (i / 20.))
        set_volume(int(vol), True)
        time.sleep(s / 20.)
    pause()  # Pause the music
    # Wait, otherwise you hear the music resume for a fraction of a second
    time.sleep(0.5)
    set_volume(volume, True)  # Set the volume back


def fade_in(s):
    # Fade in in s seconds
    if s < 0.5:
        log("Time to fade in may not be smaller than 0.5 seconds.")
        s = 0.5
    volume = variables.get("volume", 75)
    s -= 0.5  # Compensate for computing time
    for i in range(20):
        vol = volume * (i / 20.)
        set_volume(int(vol), True)
        time.sleep(s / 20.)


def get_playing():
    # Return songObject of song played
    ans = variables.get("playing", None)
    if ans is None:
        return ans
    artist, album, song = ans
    return library.get_song(artist, album, song)


def pause():
    os.system("pkill -STOP mpg123")
    variables.put("status", variables.PAUSED)


def resume():
    status = variables.get("status", variables.STOPPED)

    if status == variables.PLAYING:
        return
    elif status == variables.STOPPED:
        # Music is stopped, play song from beginning
        playing = variables.get("playing", None)
        if playing is None:
            return
        song_obj = library.get_song(playing[0], playing[1], playing[2])
        play(song_obj)
    elif status == variables.PAUSED:
        os.system("pkill -CONT mpg123")

    variables.put("status", variables.PLAYING)


def stop():
    variables.put("status", variables.STOPPED)
    variables.put("stop_timer", True, False)
    os.system("pkill mpg123")


def start_timer():
    if variables.get("stop_timer", False):
        # A timer is already waiting to start
        return

    variables.put("stop_timer", True, False)
    variables.put("elapsed", 0, False)
    time.sleep(0.5)  # Wait to give the other timer time to stop
    variables.put("stop_timer", False, False)  # The timer starts

    playing = variables.get("playing", None)
    if playing is None:
        log("Audio.py: playing == None!")
        return

    song = library.get_song(playing[0], playing[1], playing[2])

    start_time = variables.get("song_start", None)
    if start_time is None:
        log("Audio.py: song_start = None!")
        return

    # Start counting
    while True:
        time_elapsed = time.time() - start_time

        if time_elapsed >= float(song.get_duration()):
            # Song is done playing, play next song
            queue = variables.get("queue", None)
            if queue is None:
                log("Audio.py: queue = None!")
                return
            # Play new song
            queue_nr = queue.index(playing)
            queue_nr += 1
            song = queue[queue_nr % len(queue)]  # Make dat shit loop

            song_obj = library.get_song(song[0], song[1], song[2])
            play(song_obj)
            return  # Stop this timer

        if variables.get("stop_timer", False):
            # A new timer is ready to go, stop this one
            return

        # If the music is paused
        if variables.get("status", -1) == variables.PAUSED:
            start_pause_time = time.time()
            while variables.get("status", -1) == variables.PAUSED:
                time.sleep(0.1)  # Wait for the music to be continued
            start_time += time.time() - start_pause_time

        variables.put("elapsed", int(time_elapsed*1000)/1000., False)
        time.sleep(0.1)  # Sleep for a bit


def push():
    config = {
        'GCM_API_KEY': variables.get("gcm_api_key", "")
    }
    app.config.update(config)

    client = FlaskGCM()
    client.init_app(app)

    with app.app_context():
        tokens = variables.get("gcm_tokens", [])
        if not tokens:
            log("No devices registered")
            return
        playing = variables.get("playing", [])
        alert = {"artist": playing[0],
                 "album": playing[1],
                 "song": playing[2],
                 "duration": variables.get("song_duration", 0)}

        # Send to single device.
        # NOTE: Keyword arguments are optional.
        res = client.send(tokens,
                          alert,
                          collapse_key='collapse_key',
                          delay_while_idle=False,
                          time_to_live=600)

    # Send to multiple devices by passing a list of ids.
    # client.send(tokens, alert)#, **options)
