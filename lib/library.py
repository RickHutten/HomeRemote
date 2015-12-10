class Library:
	def __init__(self):
		self.albums = []   # List of albumObjects
		self.artists = []  # List of artistObjects

	def add_album(self, albumObject):
		if albumObject not in self.albums:
			self.albums.append(albumObject)

	def add_artist(self, artistObject):
		if artistObject not in self.artists:
			self.artists.append(artistObject)

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

	def add_song(self, songObject):
		# Add album and artist to lib if not exists
		if songObject.get_album() not in self.albums:
			self.albums.append(songObject.get_album())
		if songObject.get_artist() not in self.artists:
			self.artists.append(songObject.get_artist())

	def get_album(self, artist_name, album_title):
		# Get the albumObject given the album title and artist name
		for album in self.albums:
			if album.get_title() == album_title and album.get_artist().get_name() == artist_name:
				return album
		raise StandardError("Album not found: %s - %s" % (artist_name, album_title))

	def get_artist(self, artist_name):
		# Get the artistObject given the artist name
		for artist in self.artists:
			if artist.get_name() == artist_name:
				return artist
		raise StandardError("Artist not found: %s" % artist_name)

	def print_lib(self):
		print "Library sorted by artist:"
		print ""
		for artist in sorted(self.artists, key=lambda a: a.get_name()):
			print artist.get_name(), "\\"
			for album in sorted(artist.get_albums(), key=lambda a: a.get_title()):
				print "    ", album.get_title(), "\\\t\t\t", album.get_image()
				for song in sorted(album.get_songs(), key=lambda a: a.get_order()):
					print "        ", song.get_order(), "-", song.get_title(), "\t\t\t", song.get_path()

		print ""
		print "---------------------------------------"
		print ""
		print "Library sorted by album:"
		print ""
		for album in sorted(self.albums, key=lambda a: (a.get_title(), a.get_artist().get_name())):
			print album.get_title(), ":", album.get_artist().get_name(), "\\\t\t\t", album.get_image()
			for song in sorted(album.get_songs(), key=lambda a: a.get_title()):
				print "    ", song.get_title(), "\t\t\t", song.get_path()

	def print_lib_short(self):
		print "Library sorted by artist:"
		print ""
		for artist in sorted(self.artists, key=lambda a: a.get_name()):
			print artist.get_name(), "\\"
			for album in sorted(artist.get_albums(), key=lambda a: a.get_title()):
				print "    ", album.get_title(), ":",
				song_no = len(album.get_songs())
				print song_no, "songs"

		print ""
		print "---------------------------------------"
		print ""
		print "Library sorted by album:"
		print ""
		for album in sorted(self.albums, key=lambda a: (a.get_title(), a.get_artist().get_name())):
			print album.get_title(), ":", album.get_artist().get_name(), ":",
			song_no = len(album.get_songs())
			print song_no, "songs"


			
