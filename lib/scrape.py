import os, sys
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def scrape():
	print "Scraping songs..."
	start = time.clock()
	no_songs = 0

	filename = "./data/song_data"
        # If the file does not exist, make a new one
        try:
            # Try to read the file
            f = open(self.filename, "r")
        except IOError:
            # File does not exist, create new
            f = open(self.filename, "w")

	f.write("song;artist;album;order;file_path;image_path;length\n")
	
	for dirname, dirnames, filenames in os.walk('/home/pi/Music'):  # One directory per loop
	
	    # Search for album image
	    img_source = "No image"
	    for filename in filenames:
	    	extension = filename.split(".")[-1]
	        if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]:
	        	img_source = os.path.join(dirname, filename)
	        	break

	    for filename in filenames:
	    	# Continue if file is image or not a mp3 file
	    	extension = filename.split(".")[-1]
	        if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]:
	        	continue
		if extension != "mp3":
			continue

		# Get song path
		song_path = os.path.join(dirname, filename)		

		# Load song
		audio = MP3(song_path, ID3=EasyID3)

		# Get song attributes
		song_name = str(audio["title"][0])
		artist = str(audio["artist"][0])
		album = str(audio["album"][0])
		song_order = str(audio["tracknumber"][0].split("/")[0]) # Some are numbered: '09/16' meaning track 9 of 16
		length = int(audio.info.length) + 1 # Roof

		# Update user and write source to file
		no_songs += 1
		print "\r%d songs scraped"%(no_songs),
	        sys.stdout.flush()
		f.write("%s;%s;%s;%s;%s;%s;%s\n" % (song_name, artist, album, song_order, song_path, img_source, length))
	
	# Close file
	f.close()
	print "\r" + str(no_songs) + " songs scraped in", time.clock() - start, "seconds."
	sys.stdout.flush()
if __name__ == '__main__':
	scrape()
