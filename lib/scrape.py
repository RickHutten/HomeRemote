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
    f.write("song;artist;album;order;file_path;image_path;length\n")

    for dirname, dirnames, filenames in os.walk(
            '/home/pi/Music'):  # One directory per loop

        # Search for album image
        img_source = "No image"
        for filename in filenames:
            extension = filename.split(".")[-1]
            if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif",
                             "GIF"]:
                img_source = os.path.join(dirname, filename)
                break

        for filename in filenames:
            # Continue if file is image or not a mp3 file
            extension = filename.split(".")[-1]
            if extension in ["jpg", "JPG", "png", "PNG", "bmp", "BMP", "gif",
                             "GIF"]:
                continue
            if extension != "mp3":
                continue

            # Get song path
            song_path = os.path.join(dirname, filename)

            # Load song
            audio = MP3(song_path, ID3=EasyID3)

            # Get song attributes
            song_name = audio["title"][0]
            artist = audio["artist"][0]
            # try:
            album = audio["album"][0]
            # except:
            # print "Dit gaat fout"
            # print audio["album"][0]
            # Some are numbered: '09/16' meaning track 9 of 16
            song_order = str(audio["tracknumber"][0].split("/")[0])
            length = int(audio.info.length) + 1  # Roof

            # Update user and write source to file
            no_songs += 1
            print "\r%d songs scraped" % no_songs,
            sys.stdout.flush()
            line = "%s;%s;%s;%s;%s;%s;%s\n" % (song_name, artist, album,
                                               song_order, song_path,
                                               img_source, length)
            f.write(line.encode("utf8"))

    # Close file
    f.close()
    print "\r" + str(
        no_songs) + " songs scraped in", time.clock() - start, "seconds."
    sys.stdout.flush()


if __name__ == '__main__':
    scrape()
