import os
import sys
import time
from multiprocessing import Process, Value, Manager
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def scrape():
    print "Scraping songs..."
    start = time.time()
    no_threads = 3
    threads = []
    no_songs = Value('i', 0)
    thread_output = [Manager().list() for i in range(no_threads)]
    song_list = []

    # One directory per loop
    for dirname, dirnames, filenames in os.walk('/home/pi/Music'):
        for filename in filenames:
            # Continue if file is not a mp3 file
            extension = filename.split(".")[-1]
            if extension != "mp3":
                continue

            # Get song path and store in list
            song_path = os.path.join(dirname, filename)
            song_list.append(song_path)

    # Make threads
    for i in range(no_threads):
        size = len(song_list) / no_threads + 1  # Size of song list to process
        song_list_slice = song_list[i * size:(i + 1) * size]  # Slice of song_list to process
        threads.append(Process(target=read_songs, args=(song_list_slice, thread_output[i], len(song_list), no_songs,)))

    # Start threads
    for i in range(no_threads):
        threads[i].start()

    # Wait for all the threads to finish
    for i in range(no_threads):
        threads[i].join()

    # Count the number of processed songs (no_songs.value is somehow not always correct!)
    total_songs = 0
    for output in thread_output:
        total_songs += len(output)
    print "\r" + str(total_songs) + "/" + str(len(song_list)) + " songs scraped in", int(
        (time.time() - start) * 100) / 100., "seconds."

    # Write to file
    print "Writing to file..."
    filename = "./data/song_data"
    f = open(filename, "w")
    f.write("song;artist;album;order;file_path;length;albumartist\n")
    for output in thread_output:
        for line in output:
            f.write(line)
    f.close()
    print "Done!"


def read_songs(songs, output, total_songs, no_songs):
    # Process the given list of songs
    for song_path in songs:
        # Load song
        try:
            audio = MP3(song_path, ID3=EasyID3)
        except:
            print "\nError reading file:", song_path
            continue
        # Get song attributes
        song_name = audio["title"][0]
        artist = audio["artist"][0]
        album = audio["album"][0]

        # Try to get the album artist tag, if not present, use song artist
        try:
            album_artist = audio["albumartist"][0]  # This line
            if album_artist.lower() == artist.lower():  # Prevent difference in caps
                album_artist = artist
        except KeyError:
            album_artist = artist
        # Some are numbered: '09/16' meaning track 9 of 16
        song_order = str(audio["tracknumber"][0].split("/")[0])
        length = audio.info.length

        # Update user and save info in list
        no_songs.value += 1
        print "\r%d\%d songs scraped" % (no_songs.value, total_songs),
        sys.stdout.flush()

        line = song_name + ";" + artist + ";" + album + ";" + song_order + ";" + song_path + ";" + str(
            length) + ";" + album_artist
        output.append(line.encode("utf8") + "\n")


if __name__ == '__main__':
    scrape()
