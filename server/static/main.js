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

	setAlbums();	

	setClickListeners();

	sizeBody();

	poll();
});

$(window).resize(function() {
	setTileSize();
	sizeBody();
});

function sizeBody() {
	var top = document.getElementById('navbar').getBoundingClientRect().bottom;
	var bottom = document.getElementById('footer').getBoundingClientRect().top;
	$('#content').css("min-height", (bottom-top-40) + "px");
	
}

function showAlbum(artist, album) {
	$.get("http://rickert.noip.me/get2/" + artist.replace(/ /g,"_"), function(data, status){
		var albums = data.albums;
		for (i = 0; i < albums.length; i++) {
			var alb = albums[i];
			if (alb.title == album) {
				// This is the album
				$('#content').html(getAlbumView(artist, album, alb.songs));
				scrollToTop();
				break; // exit the for-loop
			}
		}
	});
}

function getStatus() {
	$.get("http://rickert.noip.me/status", function(data, status){
		var playing = data.playing;
		var status = data.status;
		var artist = playing.artist;
		var album = playing.album;
		var song = playing.song;
		$("#playing-title").html(song);
		$("#playing-artist-album").html(artist + " - " + album);
		var src = "http://rickert.noip.me/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_");
		$("#playing-image").attr("src", src);

		$('#play-pause').eq(0).attr("status", status);
		if (status == "PLAYING") {
			$('#play-pause').eq(0).attr("src", "http://rickert.noip.me/static/pause.png");
		}
		
	});
}

function setClickListeners() {
	// Set tab listeners
	$('#tab-artist').click(setArtists);
	$('#tab-album').click(setAlbums);

	// Set music control listeners
	$('#play-pause').click(function() {
		if ($('#play-pause').eq(0).attr("status") == "PLAYING") {
			$.get("http://rickert.noip.me/pause", function(data, status){
				$('#play-pause').eq(0).attr("src", "http://rickert.noip.me/static/play.png");
				$('#play-pause').eq(0).attr("status", "PAUSED");
			});
		} else {
			$.get("http://rickert.noip.me/resume", function(data, status){
				$('#play-pause').eq(0).attr("src", "http://rickert.noip.me/static/pause.png");
				$('#play-pause').eq(0).attr("status", "PLAYING");
			});
		}
	});

	$('#skip-next').click(function() {
		$.get("http://rickert.noip.me/next", null);
	});
}

function scrollToTop() {
	//$('#content').animate({scrollTop: 0}, 1000);
	window.scrollTo(0, 0);
}

function onAlbumClicked(e) {
	var p = $(e).find('p');
	var album = p[0].innerHTML;
	var artist = p[1].innerHTML;
	showAlbum(artist, album);
}

function onArtistClicked() {
	console.log("Clicked on artist");
}

function onSongClicked(e) {
	var song = $(e).find('.song-title')[0].innerHTML;
	var artist = $('#artist')[0].innerHTML;
	var album = $('#album')[0].innerHTML;

	var data = new FormData();
	data.append("artist", artist);
	data.append("album", album);
	data.append("song", song);

	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://rickert.noip.me/play", true);
	xhr.onload = function() {console.log(this.responseText)};
	data = '{"artist":"'+artist+'", "album":"'+album+'", "song":"'+song+'"}';
	xhr.send(data);	
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
		scrollToTop();
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
		scrollToTop();
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
		console.log("data returned");
		// When a new song is played on the server
		var playing = data.playing;
		var status = data.status;
		var artist = playing.artist;
		var album = playing.album;
		var song = playing.song;
		$("#playing-title").html(song);
		$("#playing-artist-album").html(artist + " - " + album);
		var src = "http://rickert.noip.me/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_");
		$("#playing-image").attr("src", src);

		$('#play-pause').eq(0).attr("status", status);
		if (status == "PLAYING") {
			$('#play-pause').eq(0).attr("src", "http://rickert.noip.me/static/pause.png");
			$('#play-pause').eq(0).attr("status", "PLAYING");
		} else if (status == "PAUSED") {
			$('#play-pause').eq(0).attr("src", "http://rickert.noip.me/static/play.png");
			$('#play-pause').eq(0).attr("status", "PAUSED");
		}
		poll();  // Start function again
	});
}

function clearSelection() {
	if (document.selection) {
		document.selection.empty();
	} else if (window.getSelection){
		window.getSelection().removeAllRanges();
	}
}
