import json
import os
from urllib2 import urlopen
from lib.log import log


class ImageManager:
    def __init__(self):
        # Make dictionary
        if not os.path.exists("./data/images/"):
            os.system("mkdir ./data/images/")
            os.system("mkdir ./data/images/albums")
            os.system("mkdir ./data/images/artists")

    def get_artist_image_filepath(self, artist):
        # If the file already exists, return filepath
        artist_underscore = artist.replace(" ", "_")
        artist_plus = artist.replace(" ", "+")
        if os.path.isfile("./data/images/artists/%s.jpg" % artist_underscore):
            return "%s/data/images/artists/%s.jpg" % (
                os.getcwd(), artist_underscore)

            # Download json to get image urls
        data = self._get_json(
            "https://api.spotify.com/v1/search?type=artist&q=%s" % (
                artist_plus))
        try:
            images = data["artists"]["items"][0]["images"]
        except IndexError:
            log("Could not find artist: %s" % artist_underscore)
            return "%s/data/images/no-artist.jpg" % (os.getcwd())

        # Get image with biggest width
        best_width = 0
        best_url = ""
        for image in images:
            if image["width"] > best_width:
                best_width = image["width"]
                best_url = image["url"]

        # Now we have the best url, download it to a file and return filepath
        self._download_image(best_url, "./data/images/artists/%s.jpg" % (
            artist_underscore))
        log("Artist image downloaded: " + artist)
        return "%s/data/images/artists/%s.jpg" % (
            os.getcwd(), artist_underscore)

    def get_album_image_filepath(self, artist, album):
        # If the file already exists, return filepath
        artist_underscore = artist.replace(" ", "_")
        artist_plus = artist.replace(" ", "+")
        album_underscore = album.replace(" ", "_")
        album_plus = album.replace(" ", "+")
        if os.path.isfile("./data/images/albums/%s.jpg" % (
                        artist_underscore + "-" + album_underscore)):
            return "%s/data/images/albums/%s.jpg" % (
                os.getcwd(), artist_underscore + "-" + album_underscore)

            # Download json to get image urls
        data = self._get_json(
            "https://api.spotify.com/v1/search?type=album&q=%s" % (
                artist_plus + "+" + album_plus.replace("&", "+")))
        items = data["albums"]["items"]
        try:
            item = items[0]
        except IndexError:
            # Try the hard way
            image_url = self._download_album_hard_way(artist, album)
            if image_url is not None:
                # Success, continue program
                log("Album download method 2 success: %s" % (
                    artist + " - " + album))
                self._download_image(
                    image_url,
                    "./data/images/albums/%s.jpg" % (
                        artist_underscore + "-" + album_underscore))
                return "%s/data/images/albums/%s.jpg" % (
                    os.getcwd(), artist_underscore + "-" + album_underscore)
            else:
                log("Failed to find album: %s" % (artist + " - " + album))
                return "%s/data/images/no-album.jpg" % (os.getcwd())

        for i in items:
            if i["name"] == album:
                # If the name matches exactly, that this one
                item = i
                break
        images = item["images"]

        # Get image with biggest width
        best_width = 0
        best_url = ""
        for image in images:
            if image["width"] > best_width:
                best_width = image["width"]
                best_url = image["url"]

        # Now we have the best url, download it to a file and return filepath
        self._download_image(best_url, "./data/images/albums/%s.jpg" % (
            artist_underscore + "-" + album_underscore))
        log("Album image downloaded: " + artist + " - " + album)
        return "%s/data/images/albums/%s.jpg" % (
            os.getcwd(), artist_underscore + "-" + album_underscore)

    @staticmethod
    def _get_json(url):
        data = urlopen(url).read()
        output = json.loads(data)
        return output

    @staticmethod
    def _download_image(url, filename):
        fileout = open(filename, "wb")
        fileout.write(urlopen(url).read())
        fileout.close()
        return

    def _download_album_hard_way(self, artist, album):
        artist_plus = artist.replace(" ", "+")
        # Download json of the artist to get the artist ID
        data = self._get_json(
            "https://api.spotify.com/v1/search?type=artist&q=%s" % (
                artist_plus))
        # Sort by popularity
        try:
            item = sorted(data["artists"]["items"], key=lambda a: a["popularity"], reverse=True)[0]
        except IndexError:
            # Noting is found
            return
        artist_id = item["id"]
        # Get the albums of the artist now that we have the artist ID

        data = self._get_json(
            "https://api.spotify.com/v1/artists/%s/albums" % artist_id)
        items = data["items"]
        for item in items:
            if item["name"] == album:
                images = item["images"]
                # Get image with biggest width
                best_width = 0
                best_url = ""
                for image in images:
                    if image["width"] > best_width:
                        best_width = image["width"]
                        best_url = image["url"]
                return best_url
        return
