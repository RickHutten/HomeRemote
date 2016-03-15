class Album:
    def __init__(self):
        self.title = ""  # String (title)
        self.artist = None  # Artist object
        self.image = ""  # String (image path)
        self.songs = []  # List of Song objects

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

    def set_image(self, s):
        # Set image path of the Album
        self.image = s

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
        song_object.set_album(self)
        self.songs.append(song_object)

    def print_songs(self):
        # Print all songs in album
        print self.title, ":",
        for song in self.songs:
            print song.get_title(),
        print ""
