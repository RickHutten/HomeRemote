from threading import Thread
import library
import artist
import album
import song
import image


def get_instance():
    lib = library.Library()
    image_manager = image.ImageManager()
    line_no = 0
    f = open("./data/song_data")

    for line in f:
        line_no += 1
        if line_no == 1:
            # First line is table titles
            continue
        line = line.split(";")

        # Get variables from line.
        song_title = line[0].strip()
        artist_name = line[1].strip()
        album_title = line[2].strip()
        song_order = line[3].strip()
        song_path = line[4].strip()
        duration = line[5].strip()
        album_artist = line[6].strip()

        s = song.Song()
        al = album.Album()
        ar = artist.Artist()
        alar = artist.Artist()

        s.set_title(song_title)
        s.set_order(song_order)
        s.set_path(song_path)
        s.set_duration(duration)

        # Get the artist object
        for art in lib.get_artists():
            if art.get_name() == artist_name:
                # Artist already created
                ar = art
                break
        else: # If loop is ended without break, make new one
            # Set artist name only if artist is new
            ar.set_name(artist_name)
            # Start new thread that downloads the image
            thread = Thread(target=ar.set_image, args=(image_manager,))
            thread.start()

        if album_artist != artist_name:
            # Get album artist or make new one
            for art in lib.get_artists(True):
                if art.get_name() == album_artist:
                    # Artist already created
                    alar = art
                    break
            else: # If loop is ended without break, make new one
                # Set artist name only if artist is new
                alar.set_name(album_artist)
                alar.set_is_album_artist(True)
                # Start new thread that downloads the image
                thread = Thread(target=alar.set_image, args=(image_manager,))
                thread.start()
        else: # Album and song artist are the same
            alar = ar

        # Get the album object
        for alb in lib.get_albums():
            if alb.get_title() == album_title and alb.get_artist().get_name() == album_artist:
                # Album already created
                al = alb
                break
        else: # If loop is ended without break, make new one
            # Set title and image only if album is new
            al.set_title(album_title)
            al.set_artist(alar)
            # Start new thread that downloads the image
            thread = Thread(target=al.set_image, args=(image_manager,))
            thread.start()

        alar.add_album(al)
        ar.add_album(al)
        #al.set_artist(alar)

        al.add_song(s)

        s.set_album(al)
        s.set_artist(ar)
        
        lib.add_album(al)
        lib.add_artist(ar)
        lib.add_artist(alar)

    f.close()
    return lib

