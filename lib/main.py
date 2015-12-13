import library, artist, album, song, scrape
import time

def get_instance():
        scrape.scrape()
        start = time.clock()

        lib = library.Library()
	print " * Music Library refreshed!"

        line_no = 0
        f = open("./data/song_data")
        
        for line in f:
                line_no += 1
        
                if line_no == 1:
                        # First line is table titles
                        continue
        
                line = line.split(";")
        
                # Get variables from line. Strip() removes leading and trailing whitespace
                song_title = line[0].strip()
                artist_name = line[1].strip()
                album_title = line[2].strip()
                song_order = line[3].strip()
                song_path = line[4].strip()
                image_path = line[5].strip()
        
                s = song.Song()
                al = album.Album()
                ar = artist.Artist()
        
                s.set_title(song_title)
                s.set_order(song_order)
                s.set_path(song_path)
        
                for alb in lib.get_albums():
                        if alb.get_title() == album_title and alb.get_artist().get_name() == artist_name:
                                # Album already created
                                al = alb
                                break
                else:
                        # Set title and image only if album is new
                        al.set_title(album_title)
                        al.set_image(image_path)			
        
                for art in lib.get_artists():
                        if art.get_name() == artist_name:
                                # Artist already created
                                ar = art
                                break
                else:
                        # Set artist name only if artist is new
                        ar.set_name(artist_name)
        
        
                al.add_song(s)
        
                ar.add_album(al)	
        
                lib.add_song(s)
        
        f.close()
        stop = time.clock()
        return lib

