import time
import os
import lib.variables
from threading import Thread
from server import library

# Get variables
variables = lib.variables.ServerVariables()

def play(song):
	variables.put("playing", [song.get_artist().get_name(), song.get_album().get_title(), song.get_title()])
	variables.put("song_start", time.time())
	os.system("pkill mpg123")  # Kill everything that might be playing
	os.system('mpg123 -q "%s" &' % song.get_path())  # Play the song
	
	# Start counting in new thread
	thread = Thread(target=start_timer)
	thread.start()

def set_volume(vol):
	# Set volume in percentage
	if 0 <= vol <= 100:
		# Volume has to be between 0 and 100
		if vol == 0:
			os.system("amixer -1 sset PCM 0%")
			return True
		# Map 0-100% to 50-100%
		percentage = 50 + vol/2.
		command = "amixer -q sset PCM " + str(percentage) + "%"
		os.system(command)
		return True
	return False

def get_playing():
	# Return songObject of song played
	ans = variables.get("playing", None)
	if ans == None:
		return ans
	artist, album, song = ans
	return library.get_song(artist, album, song)

def pause():
	os.system("pkill -STOP mpg123")

def resume():
	os.system("pkill -CONT mpg123")

def stop():
	variables.put("playing", None)
	variables.put("stop_timer", True)
	os.system("pkill mpg123")

def start_timer():
	if variables.get("stop_timer", False):
		# A timer is already waiting to start
		return

	variables.put("stop_timer", True)
	time.sleep(1) # Wait to give the other timer time to stop
	variables.put("stop_timer", False) # The timer starts

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
		if time_elapsed >= int(song.get_duration()):
			# Song is done playing, play next song
			queue = variables.get("queue", None)
			if queue == None:
				print "Audio.py: queue = None!"
				return
			# Play new song
			queue_nr = queue.index(playing)
			queue_nr += 1
			song = queue[queue_nr%len(queue)] # Loop
			print "Playing next song:", song
			songObj = library.get_song(song[0], song[1], song[2])
			play(songObj)
			return  # Stop this timer

		time.sleep(0.1)  # Sleep for a bit
		# print "Counting ", int(song.get_duration()) - time_elapsed, "seconds to go"
		if variables.get("stop_timer", False):
			# A new timer is ready to go, stop this one
			variables.put("stop_timer", False)
			return
	
