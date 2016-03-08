import time
import os
import lib.variables
from threading import Thread
from server import library, variables, app
from flask_pushjack import FlaskGCM

def play(song):
	variables.put("status", "playing")
	variables.put("playing", [song.get_artist().get_name(), song.get_album().get_title(), song.get_title()])
	variables.put("song_start", time.time())
	os.system("pkill mpg123")  # Kill everything that might be playing
	os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
	push()  # Notify the users
	
	# Start counting in new thread
	thread = Thread(target=start_timer)
	thread.start()

def set_volume(vol, fade=False):
	# Set volume in percentage
	if 0 <= vol <= 100:
		# Volume has to be between 0 and 100
		if not fade:
			variables.put("volume", vol)		
		if vol == 0:
			os.system("amixer -q sset PCM 0%")
			return True
		# Map 0-100% to 50-100%
		percentage = 50 + vol/2.
		command = "amixer -q sset PCM " + str(percentage) + "%"
		os.system(command)
		return True
	return False

def fade_out(s):
	# Fade out in s seconds, music is paused afterwards and original volume restored.
	if s < 0.5:
		print "Time to fade out may not be smaller than 0.5 seconds."
		s = 0.5
	volume = variables.get("volume", 75)
	start = time.time()
	for i in range(20):
		vol = volume*(1 - (i/20.))
		set_volume(int(vol), True)
		time.sleep(s/20. - 0.5/20)  # Fade out takes about 0.5 seconds "-0.5/20" compensates for that	
	pause()  # Pause the music
	time.sleep(0.5)  # Wait a bit, otherwise you hear the music resume on high volume for a fraction of a second
	set_volume(volume, True)  # Set the volume back

def fade_in(s):
	# Fade in in s seconds
	if s < 0.5:
		print "Time to fade in may not be smaller than 0.5 seconds."
		s = 0.5
	volume = variables.get("volume", 75)
	start = time.time()
	for i in range(20):
		vol = volume*((i/20.))
		set_volume(int(vol), True)
		time.sleep(s/20. - 0.5/20)  # Fade out takes about 0.5 seconds "-0.5/20" compensates for that	

def get_playing():
	# Return songObject of song played
	ans = variables.get("playing", None)
	if ans == None:
		return ans
	artist, album, song = ans
	return library.get_song(artist, album, song)

def pause():
	os.system("pkill -STOP mpg123")
	variables.put("status", "paused")

def resume():
	os.system("pkill -CONT mpg123")
	variables.put("status", "playing")

def stop():
	variables.put("status", "stopped")
	variables.put("playing", None)
	variables.put("stop_timer", True)
	os.system("pkill mpg123")

def start_timer():
	if variables.get("stop_timer", False):
		# A timer is already waiting to start
		return

	variables.put("stop_timer", True)
	time.sleep(1)  # Wait to give the other timer time to stop
	variables.put("stop_timer", False)  # The timer starts

	playing = variables.get("playing", None)
	if playing == None:
		print "Audio.py: playing == None!"
		return

	song = library.get_song(playing[0], playing[1], playing[2])
	
	start_time = variables.get("song_start", None)
	if start_time == None:
		print "Audio.py: song_start = None!"
		return 
	
	# Start counting
	while True:
		time_elapsed = time.time() - start_time
		if time_elapsed >= float(song.get_duration()):
			# Song is done playing, play next song
			queue = variables.get("queue", None)
			if queue == None:
				print "Audio.py: queue = None!"
				return
			# Play new song
			queue_nr = queue.index(playing)
			queue_nr += 1
			song = queue[queue_nr%len(queue)]  # Make dat shit loop
			print "Playing next song:", song
			songObj = library.get_song(song[0], song[1], song[2])
			play(songObj)
			return  # Stop this timer

		time.sleep(0.1)  # Sleep for a bit

		# print "Counting ", float(song.get_duration()) - time_elapsed, "seconds to go"
		if variables.get("stop_timer", False):
			# A new timer is ready to go, stop this one
			return
		# If the music is paused
		if variables.get("status", "") == "paused":
			start_pause_time = time.time()
			while variables.get("status", "") == "paused":
				time.sleep(0.1)  # Wait for the music to be continued
			start_time += time.time() - start_pause_time  # Correct for the paused time

def push():
	config = {
		'GCM_API_KEY' : variables.get("gcm_api_key", "")
	}
	app.config.update(config)
	
	client = FlaskGCM()
	client.init_app(app)

	with app.app_context():
		tokens = variables.get("gcm_tokens", [])
		if tokens == []:
			print "No devices registered"
			return
		playing = variables.get("playing", [])
		alert = {"artist" : playing[0], "album" : playing[1], "song" : playing[2]}

		# Send to single device.
		# NOTE: Keyword arguments are optional.
		res = client.send(tokens,
	                  alert,
	                  collapse_key='collapse_key',
	                  delay_while_idle=True,
	                  time_to_live=604800)
		
	# Send to multiple devices by passing a list of ids.
	#client.send(tokens, alert)#, **options)
	
