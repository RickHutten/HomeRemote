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
	$.get(getUrl("/get2/" + artist.replace(/ /g,"_")), function(data, status){
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
	$.get(getUrl("/status"), function(data, status){
		var playing = data.playing;
		var status = data.status;
		var artist = playing.artist;
		var album = playing.album;
		var song = playing.song;
		$("#playing-title").html(song);
		$("#playing-artist").html(artist);
		$("#playing-album").html(album);
		var src = getUrl("/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_"));
		$("#playing-image").attr("src", src);

		$('#play-pause').eq(0).attr("status", status);
		if (status == "PLAYING") {
			$('#play-pause').eq(0).attr("src", getUrl("/static/pause.png"));
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
			$.get(getUrl("/pause"), function(data, status){
				$('#play-pause').eq(0).attr("src", getUrl("/static/play.png"));
				$('#play-pause').eq(0).attr("status", "PAUSED");
			});
		} else {
			$.get(getUrl("/resume"), function(data, status){
				$('#play-pause').eq(0).attr("src", getUrl("/pause.png"));
				$('#play-pause').eq(0).attr("status", "PLAYING");
			});
		}
	});
	$('#skip-next').click(function() {
		$.get(getUrl("/next"), null);
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
	var song = $(e).eq(0).attr("title");
	var artist = $(e).eq(0).attr("artist");
	var album = $(e).eq(0).attr("album");

	var xhr = new XMLHttpRequest();
	xhr.open("POST", getUrl("/play"), true);
	xhr.onload = function() {console.log(this.responseText)};
	data = '{"artist":"'+artist+'", "album":"'+album+'", "song":"'+song+'"}';
	xhr.send(data);

	postQueue();
}

function postQueue() {
	// POSTs all songviews on the screen to the server
	var songs = $('.song-view');
	// {"songs": [ {"artist": artist, "album": album, "song": song}, ...]}
	var data = '';
	for (i = 0; i < songs.length; i++) {
		var song = songs.eq(i);
		var title = song.attr("title");
		var artist = song.attr("artist");
		var album = song.attr("album");
		data += '{"artist":"'+artist+'", "album":"'+album+'", "song":"'+title+'"}';
		// Add comma for next song
		if (i != songs.length-1) {data += ',';}
	}
	var json = '{"songs": [ ' + data + "]}";

	var xhr = new XMLHttpRequest();
	xhr.open("POST", getUrl("/set2/queue"), true);
	xhr.onload = function() {console.log(this.responseText)};
	xhr.send(json);
}

function setAlbums() {
	$.get(getUrl("/albums2"), function(data, status){
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
	$.get(getUrl("/artists2"), function(data, status){
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
	$.get(getUrl("/poll"), function(data, status){
		console.log("data returned");
		// When a new song is played on the server
		var playing = data.playing;
		var status = data.status;
		var artist = playing.artist;
		var album = playing.album;
		var song = playing.song;
		$("#playing-title").html(song);
		$("#playing-artist").html(artist);
		$("#playing-album").html(album);
		var src = getUrl("/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_"));
		$("#playing-image").attr("src", src);

		$('#play-pause').eq(0).attr("status", status);
		if (status == "PLAYING") {
			$('#play-pause').eq(0).attr("src", getUrl("/static/pause.png"));
			$('#play-pause').eq(0).attr("status", "PLAYING");
		} else if (status == "PAUSED") {
			$('#play-pause').eq(0).attr("src", getUrl("/static/play.png"));
			$('#play-pause').eq(0).attr("status", "PAUSED");
		}
		poll();  // Start function again
	});
}

function getUrl(subdomain) {
	//return "https://rickert.noip.me" + subdomain;  // For public site on RPi
	return "" + subdomain;  // For localhost
}