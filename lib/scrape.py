import os
import sys
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def scrape():
    print "Scraping songs..."
    start = time.clock()
    no_songs = 0

    filename = "./data/song_data"
    f = open(filename, "w")
    f.write("song;artist;album;order;file_path;length;albumartist\n")

    # One directory per loop
    for dirname, dirnames, filenames in os.walk('/home/pi/Music'):
        for filename in filenames:
            # Continue if file is image or not a mp3 file
            extension = filename.split(".")[-1]
            if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif",
                             "GIF"]:
                continue
            if extension != "mp3":
                continue
            #print filename
            # Get song path
            song_path = os.path.join(dirname, filename)

            # Load song
            audio = MP3(song_path, ID3=EasyID3)

            # Get song attributes
            song_name = audio["title"][0]
            artist = audio["artist"][0]
            album = audio["album"][0]

            # Try to get the album artist tag, if not present, use song artist
            try:
                album_artist = audio["albumartist"][0] # This line
                if album_artist.lower() == artist.lower():  # Prevent difference in caps
                    album_artist = artist
            except KeyError:
                album_artist = artist

            # Some are numbered: '09/16' meaning track 9 of 16
            song_order = str(audio["tracknumber"][0].split("/")[0])
            length = audio.info.length

            # Update user and write source to file
            no_songs += 1
            print "\r%d songs scraped" % no_songs,
            sys.stdout.flush()

            line = song_name + ";" + artist + ";" + album + ";" + song_order + ";" + song_path + ";" + str(length) + ";" + album_artist
            f.write(line.encode("utf8") + "\n")

    # Close file
    f.close()
    print "\r" + str(
        no_songs) + " songs scraped in", time.clock() - start, "seconds."
    sys.stdout.flush()


if __name__ == '__main__':
    scrape()
