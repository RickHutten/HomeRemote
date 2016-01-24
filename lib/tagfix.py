import os
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def fix():
	errors = 0
	warnings = 0
	for dirname, dirnames, filenames in os.walk('/home/pi/Music'):  # One directory per loop
	
	    # Search for album image
	    img_source = "No image"
	    mp3s = 0
	    for filename in filenames:
	    	extension = filename.split(".")[-1]
	        if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]:
	        	img_source = os.path.join(dirname, filename)
	        if extension == "mp3":
			mp3s += 1
	    
	    if mp3s != 0 and img_source == "No image":
		print "No image found for files in path " + dirname
		warnings += 1
	    	
	    no_images = 0
	    for filename in filenames:
	    	# Continue if file is image
	    	extension = filename.split(".")[-1]
	        if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]:
	        	no_images += 1
			if no_images == 2:
				# A second image is found
				print "Multiple images found, please clean up folder:", dirname
				warnings += 1
			continue
		if extension != "mp3":
		    print "Non music file encoutered:", filename, "in", dirname
		    warnings += 1
		    continue

		# Get song path
		song_path = os.path.join(dirname, filename)		

		# Load song
		audio = MP3(song_path, ID3=EasyID3)

		# Get song attributes
		for tag in ["title", "artist", "album", "tracknumber"]:
			try:
				iex = str(audio[tag])
				if ":" in iex or ";" in iex:
					errors += 1
					print audio.pprint()
					print "File: " + os.path.join(dirname, filename)
					print 'Tag "%s" contains invalid characters!'%tag
					tagvalue = raw_input("What should be the %s of the song? "%tag)
					print ""
					audio[tag] = tagvalue.decode('unicode-escapade')
					audio.save()
			except:
				errors += 1
				print audio.pprint()
				print "File: " + os.path.join(dirname, filename)
				print 'Tag "%s" is missing!'%tag
				tagvalue = raw_input("What should be the %s of the song? "%tag)
				print ""
				audio[tag] = tagvalue.decode('unicode-escape')
				audio.save()

		try:
			length = int(audio.info.length)
			if length < 2:
				# Length of audio file is very short, probably false
				raise ValueError
		except:
			errors += 1
			print audio.pprint()
			print "File: " + os.path.join(dirname, filename)
			print ""
			print "Length of audio file is unknown."
			print "Trying to do something about it, don't know if it works"
			ans = input("How many seconds long is this audio file? ")
			print "Cool cool cool, trying to fix it.."
			audio.info.length = ans
			audio.save()
			print "Succes!"
	print "Scan finished with %d warning(s). Fixed %d error(s)." %(warnings, errors)

if __name__ == '__main__':
	fix()
