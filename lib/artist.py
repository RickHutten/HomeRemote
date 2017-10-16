from lib.log import log


class Artist:
    def __init__(self):
        self.name = ""  # String of artist name
        self.albums = []  # List containing AlbumObjects
        self.image = ""  # String (image path)
        self.is_album_artist = False

    def __str__(self):
        return "ArtistObject: " + self.name

    def __repr__(self):
        return self.__str__()

    def add_album(self, album_object):
        for album in self.get_albums():
            if album.get_title() == album_object.get_title():
                # Album already present
                return
        # Add albumObject in album list
        self.albums.append(album_object)

    def get_albums(self):
        return self.albums

    def get_album(self, s):
        for alb in self.get_albums():
            if alb.get_title() == s:
                return alb
        log("Album not found: " + s)

    def get_songs(self):
        songs = []
        # Get all songsObjects of the artist
        for album in self.get_albums():
            for song_obj in album.get_songs():
                if song_obj.get_artist().get_name() == self.get_name():
                    songs.append(song_obj)
        return songs

    def set_name(self, s):
        self.name = s

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image

    def set_image(self, image_manager):
        # Downloads file and sets the image path
        self.image = image_manager.get_artist_image_filepath(self.get_name())

    def set_is_album_artist(self, b):
        # Set if the album is just an album artist
        self.is_album_artist = b

    def get_is_album_artist(self):
        return self.is_album_artist
