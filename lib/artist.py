class Artist:
    def __init__(self):
        self.name = ""  # String of artist name
        self.albums = []  # List containing AlbumObjects
        self.image = ""  # String (image path)

    def add_album(self, album_object):
        # Add albumObject in album list
        for album in self.albums:
            if album.get_title() == album_object.get_title():
                # Album already present
                # print "Dont add album again:", album.get_title()
                return
        album_object.set_artist(self)
        self.albums.append(album_object)

    def get_albums(self):
        return self.albums

    def get_album(self, s):
        for alb in self.albums:
            if alb.get_title() == s:
                return alb
        raise StandardError("Album not found: " + s)

    def get_songs(self):
        songs = []
        # Get all songsObjects of the artist
        for album in self.albums:
            for song_obj in album.get_songs():
                songs.append(song_obj)
        return songs

    def set_name(self, s):
        self.name = s

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image

    def download_image(self, image_manager):
        # Downloads file and sets the image path
        self.image = image_manager.get_artist_image_filepath(self.name)
        
