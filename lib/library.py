from lib.log import log

class Library:
    def __init__(self):
        self.albums = []  # List of albumObjects
        self.artists = []  # List of artistObjects

    def add_album(self, album_object):
        if album_object not in self.albums:
            self.albums.append(album_object)

    def add_artist(self, artist_object):
        if artist_object not in self.artists:
            self.artists.append(artist_object)

    def get_albums(self):
        return self.albums

    def get_songs(self):
        songs = []
        # Returns list of all songObjects in the library
        for album in self.albums:
            for song in album.get_songs():
                songs.append(song)
        return songs

    def get_artists(self):
        return self.artists

    def add_song(self, song_object):
        # Add album and artist to lib if not exists
        if song_object.get_album() not in self.albums:
            self.albums.append(song_object.get_album())
        if song_object.get_artist() not in self.artists:
            self.artists.append(song_object.get_artist())

    def get_album(self, artist_name, album_title):
        # Get the albumObject given the album title and artist name
        for artist in self.artists:
            if artist.get_name() == artist_name:
                for album in artist.get_albums():
                    if album.get_title() == album_title:
                        return album
        log("Album not found: %s - %s" % (artist_name, album_title))

    def get_artist(self, artist_name):
        # Get the artistObject given the artist name
        for artist in self.artists:
            if artist.get_name() == artist_name:
                return artist
        log("Artist not found: %s" % artist_name)

    def get_song(self, artist_name, album_title, song_name):
        # Get the songObject given the artist, album and title of the song
        for artist in self.artists:
            if artist.get_name() == artist_name:
                for album in artist.get_albums():
                    if album.get_title() == album_title:
                        for song in album.get_songs():
                            if song.get_title() == song_name:
                                return song
        log("Song not found: %s, %s, %s" % (artist_name, album_title, song_name))

    def print_lib(self):
        print "Library sorted by artist:"
        print ""
        for artist in sorted(self.artists, key=lambda a: a.get_name()):
            print artist.get_name(), "\\"
            for album in sorted(artist.get_albums(),
                                key=lambda a: a.get_title()):
                print "    ", album.get_title()
                for song in sorted(album.get_songs(),
                                   key=lambda a: a.get_order()):
                    print "        ", song.get_order(), "-", song.get_title()

        print "\n---------------------------------------\n"
        print "Library sorted by album:\n"
        for album in sorted(self.albums, key=lambda a:
                            (a.get_title(), a.get_artist().get_name())):
            print album.get_title(), ":", album.get_artist().get_name()
            for song in sorted(album.get_songs(), key=lambda a: a.get_title()):
                print "    ", song.get_title()

    def print_lib_short(self):
        print "Library sorted by artist:\n"
        for artist in sorted(self.artists, key=lambda a: a.get_name()):
            print artist.get_name(), "\\"
            for album in sorted(artist.get_albums(),
                                key=lambda a: a.get_title()):
                print "    ", album.get_title(), ":",
                song_no = len(album.get_songs())
                print song_no, "songs"

        print "\n---------------------------------------\n"
        print "Library sorted by album:\n"
        for album in sorted(self.albums, key=lambda a:
                            (a.get_title(), a.get_artist().get_name())):
            print album.get_title(), ":", album.get_artist().get_name(), ":",
            song_no = len(album.get_songs())
            print song_no, "songs"
