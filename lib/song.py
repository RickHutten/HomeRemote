class Song:
    def __init__(self):
        self.title = ""  # String (title)
        self.album = None  # Album object
        self.order = -1  # Int (order)
        self.path = ""  # Path of the song
        self.duration = -1  # Duration of song (seconds)

    def set_title(self, s):
        # Set title of song
        self.title = s

    def get_title(self):
        return self.title

    def set_album(self, album_object):
        # Set album of song
        self.album = album_object

    def get_album(self):
        return self.album

    def set_order(self, i):
        # Set track number
        self.order = int(i)

    def get_order(self):
        return self.order

    def set_duration(self, f):
        # Set duration of song
        self.duration = float(f)

    def get_duration(self):
        return self.duration

    def get_artist(self):
        return self.album.get_artist()

    def set_path(self, s):
        # Set path of song
        self.path = s

    def get_path(self):
        return self.path
