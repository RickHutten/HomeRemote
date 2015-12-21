class Artist:
	def __init__(self):
		self.name = ""	      # String of artist name
		self.albums = []      # List containing AlbumObjects

	def add_album(self, albumObject):
		# Add albumObject in album list
		for album in self.albums:
			if album.get_title() == albumObject.get_title():
				# Album already present
				#print "Dont add album again:", album.get_title()
				return
		albumObject.set_artist(self)
		self.albums.append(albumObject)

	def get_albums(self):
		return self.albums

	def get_album(self, s):
		for alb in self.albums:
			if alb.get_title() == s:
				return alb
		raise StandardError("Album not found: " + s)

	def set_name(self, s):
		self.name = s

	def get_name(self):
		return self.name
