import os

def scrape():
	f = open("./data/song_data", "w")
	f.write("song;artist;album;order;file_path;image_path\n")
	
	for dirname, dirnames, filenames in os.walk('/home/pi/Music'):  # One directory per loop
	    #print os.path.join(dirname)
	
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
	
	        song_path = os.path.join(dirname, filename)
		song_order = filename[:2]
		song_name = filename[:-4][3:]
	        artist = song_path.split("/")[4]
	        album = song_path.split("/")[5]
	        f.write("%s;%s;%s;%s;%s;%s\n" % (song_name, artist, album, song_order, song_path, img_source))
	
	f.close()

if __name__ == '__main__':
	scrape()
