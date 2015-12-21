import os
import time
from mutagen.mp3 import MP3

def scrape():
	start = time.clock()
	no_songs = 0
	f = open("./data/song_data", "w")
	f.write("song;artist;album;order;file_path;image_path;length\n")
	for dirname, dirnames, filenames in os.walk('/home/pi/Music'):  # One directory per loop
	
	    # Search for album image
	    img_source = "No image"
	    for filename in filenames:
	    	extension = filename.split(".")[1]
	        if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]:
	        	img_source = os.path.join(dirname, filename)
	        	break
	
	    for filename in filenames:
	    	# Continue if file is image
	    	extension = filename.split(".")[-1]
	        if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]:
	        	continue
		if extension != "mp3":
		    print "Non music file encoutered:"
		    print os.path.join(dirname, filename)
		    continue

		# Get song path
		song_path = os.path.join(dirname, filename)		

		# Load song
		audio = MP3(song_path)

		# Get song attributes
		song_name = audio["TIT2"]
		artist = audio["TPE1"]
		album = audio["TALB"]
		song_order = str(audio["TRCK"]).split("/")[0] # Some are numbered: '09/16' meaning track 9 of 16
		length = audio.info.length


		# Old way of scraping
		#song_order = filename[:2]
		#song_name = filename[:-4][3:]
	        #artist = song_path.split("/")[4]
	        #album = song_path.split("/")[5]


		no_songs += 1
	        f.write("%s;%s;%s;%s;%s;%s;%s\n" % (song_name, artist, album, song_order, song_path, img_source, length))
	
	f.close()
	print no_songs, "songs scraped in", time.clock() - start, "seconds."

if __name__ == '__main__':
	scrape()
