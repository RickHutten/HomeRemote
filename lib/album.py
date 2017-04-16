class Album:
    def __init__(self):
        self.title = ""  # String (title)
        self.artist = None  # Album, Artist object
        self.image = ""  # String (image path)
        self.songs = []  # List of Song objects

    def __str__(self):
        return "AlbumObject: " + self.title + " by " + self.get_artist().get_name()

    def __repr__(self):
        return self.__str__()

    def set_title(self, s):
        # Set title of the Album
        self.title = s

    def get_title(self):
        return self.title

    def set_artist(self, artist_object):
        # Set artist of the Album
        self.artist = artist_object

    def get_artist(self):
        return self.artist

    def get_image(self):
        return self.image

    def get_songs(self):
        return self.songs

    def get_song(self, s):
        for song in self.songs:
            if song.get_title() == s:
                return song
        raise StandardError("Song not found: " + s)

    def add_song(self, song_object):
        # Add songObject to list
        self.songs.append(song_object)

    def print_songs(self):
        # Print all songs in album
        print self.title, ":",
        for song in self.songs:
            print song.get_title(),
        print ""

    def set_image(self, image_manager):
        # Downloads file and sets the image path
        self.image = image_manager.get_album_image_filepath(self.get_artist().get_name(),
                                                            self.title)
