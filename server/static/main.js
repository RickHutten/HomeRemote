$(document).ready(function() {
	$(".tabbar-item").hover(
		function() {
			$( this ).addClass("underline");
		}
		,
		function() {
			$( this ).removeClass("underline");
		}
	);

	getStatus();

	//setArtists();

	setClickListeners();

	poll();
});

$(window).resize(function() {
	setTileSize();
});

function getStatus() {
	$.get("http://rickert.noip.me/status", function(data, status){
		// When a new song is played on the server
		var playing = data.playing;
		var artist = playing.artist;
		var album = playing.album;
		var song = playing.song;
		$("#playing-title").html(song);
		$("#playing-artist-album").html(artist + " - " + album);
		var src = "http://rickert.noip.me/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_");
		$("#playing-image").attr("src", src);
	});
}

function setClickListeners() {
	$('#tab-artist').click(setArtists);
	$('#tab-album').click(setAlbums);
}

function setAlbums() {
	$.get("http://rickert.noip.me/albums2", function(data, status){
		var albums = data.albums;
		var htmlString = '';
		for (i = 0; i < albums.length; i++) {
			var artist = albums[i].artist;
			var album = albums[i].title;			
			htmlString += getAlbumTile(artist, album);
		}
		$('#content').html(htmlString);

		// Call this twice otherwise it won't work well on narrow screen sizes
		setTileSize();
		setTileSize();
	});
}

function setArtists() {
	$.get("http://rickert.noip.me/artists2", function(data, status){
		var artists = data.artists;
		var htmlString = '';
		for (i = 0; i < artists.length; i++) {
			var artist = artists[i].name;			
			htmlString += getArtistTile(artist);
		}
		$('#content').html(htmlString);

		// Call this twice otherwise it won't work well on narrow screen sizes
		setTileSize();
		setTileSize();
	});
}

function setTileSize() {
	var pageWidth = $("#content").width();
	var itemMinWidth = 150; // in pixels
	var numberOfColumns = Math.floor(pageWidth / itemMinWidth);
	var itemWidth = pageWidth / numberOfColumns;
	var itemHeight = 1.5 * itemWidth;
	
	$(".tile-container").width(itemWidth).height(itemHeight);
}

function poll() {
	$.get("http://rickert.noip.me/poll", function(data, status){
		// When a new song is played on the server
		var artist = data.artist;
		var album = data.album;
		var song = data.song;
		$("#playing-title").html(song);
		$("#playing-artist-album").html(artist + " - " + album);
		var src = "http://rickert.noip.me/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_");
		$("#playing-image").attr("src", src);
		poll();  // Start function again
	});
}
