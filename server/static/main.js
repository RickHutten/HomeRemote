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
	
	setQueueContainerSize();

	setClickListeners();

	poll();
});

$(window).resize(function() {
	console.log("OnResize");
	setTileSize();
	setQueueContainerSize();
});

function onKnobDown(e) {
	//console.log(e);
	document.body.onmouseup = function(e){
		document.body.onmouseup = null;
		document.body.onmousemove = null;
		var posX = e.pageX;
		var left = $('#volume-bar-background').offset().left;
		var right = left + $('#volume-bar-background').width();
		var mouseOffsetFrac = (posX - left) / (right - left);
		if (mouseOffsetFrac < 0) {
			mouseOffsetFrac = 0;
		} else if (mouseOffsetFrac > 1) {
			mouseOffsetFrac = 1;
		}
		var volume = Math.round(mouseOffsetFrac * 100);
		$.get(getUrl("/set/volume/" + volume), null);
	};
	document.body.onmousemove = function(e){
		var posX = e.pageX;
		var left = $('#volume-bar-background').offset().left;
		var right = left + $('#volume-bar-background').width();
		var mouseOffsetFrac = (posX - left) / (right - left);
		if (mouseOffsetFrac < 0) {
			mouseOffsetFrac = 0;
		} else if (mouseOffsetFrac > 1) {
			mouseOffsetFrac = 1;
		}
		setVolumeVisual(mouseOffsetFrac);
	};
}

function setVolumeVisual(fraction) {
	document.getElementById("volume-knob").style.right = "calc("+ (90 - (fraction * 80)) +"% - 10px";
	document.getElementById("volume-bar").style.width = (fraction * 80) +"%";
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
	})
}

function setQueueContainerSize() {
	var playing_image_bottom = $("#playing-image-container").offset().top + $("#playing-image-container").height();
	var volume_top = $("#volume-control").offset().top;
	$("#queue").height(volume_top - playing_image_bottom);
	
	var playing_text_height = $("#playing-text-container").outerHeight();
	$("#playing-text-container").css({ top: (playing_image_bottom - playing_text_height - $("body").scrollTop()) + 'px' });
}

function fillContentFromStatus(data) {
	if (data.playing == null) {
		return;
	}
	var playing = data.playing;
	var state = data.status;
	var volume = data.volume;
	var artist = playing.artist;
	var album = playing.album;
	var song = playing.song;
	
	setVolumeVisual(volume / 100);
	
	$("#playing-title").html(song);
	$("#playing-artist").html(artist);
	$("#playing-album").html(album);
	$("#playing-text-container").show();
	var src = getUrl("/image/" + artist.replace(/ /g,"_") + "/" + album.replace(/ /g,"_"));
	$("#playing-image").attr("src", src);

	// Set play pause button
	$('#play-pause').eq(0).attr("state", state);
	if (state == "PLAYING") {
		$('#play-pause').eq(0).attr("src", getUrl("/static/pause.png"));
	} else if (state == "PAUSED") {
		$('#play-pause').eq(0).attr("src", getUrl("/static/play.png"));
	}
	
	// Adjust #playing-text-container top
	setQueueContainerSize();
}

function getStatus() {
	$.get(getUrl("/status"), function(data, status){
		fillContentFromStatus(data);
	});
	getQueue();
}

function getQueue() {
	$.get(getUrl("/queue"), function(data, status){
		var queue = data.queue;
		$("#queue").html(getQueueSongs(queue));
	});
}

function setClickListeners() {
	// Set tab listeners
	$('#tab-artist').click(setArtists);
	$('#tab-album').click(setAlbums);

	// Set music control listeners
	$('#play-pause').click(function() {
		if ($('#play-pause').eq(0).attr("state") == "PLAYING") {
			$('#play-pause').eq(0).attr("src", getUrl("/static/play.png"));
			$.get(getUrl("/pause"), function(data, status){
				$('#play-pause').eq(0).attr("src", getUrl("/static/play.png"));
				$('#play-pause').eq(0).attr("state", "PAUSED");
			});
		} else {
			$.get(getUrl("/resume"), function(data, status){
				$('#play-pause').eq(0).attr("src", getUrl("/static/pause.png"));
				$('#play-pause').eq(0).attr("state", "PLAYING");
			});
		}
	});
	
	$('#btn-prev').click(function() {
		$.get(getUrl("/previous"), null);
	});
	$('#btn-next').click(function() {
		$.get(getUrl("/next"), null);
	});
}

function scrollToTop() {
	window.scrollTo(0, 0);
}

function onAlbumClicked(e) {
	var p = $(e).find('p');
	var album = p[0].innerHTML;
	var artist = p[1].innerHTML;
	showAlbum(artist, album);
}

function onArtistClicked() {
}

function onSongClicked(e) {
	var song = $(e).eq(0).attr("title");
	var artist = $(e).eq(0).attr("artist");
	var album = $(e).eq(0).attr("album");

	var xhr = new XMLHttpRequest();
	xhr.open("POST", getUrl("/play"), true);
	//xhr.onload = function() {console.log("PostSong returns:" + this.responseText)};
	data = '{"artist":"'+artist+'", "album":"'+album+'", "song":"'+song+'"}';
	xhr.send(data);

	postQueue(e);
}

function postQueue(e) {
	// POSTs all songviews on the screen to the server
	var class_name = $(e).attr("class").split(/\s+/)[0];
	var songs = $('.'+class_name);
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
	//xhr.onload = function() {console.log("PostQueue returns: " + this.responseText)};
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
		// When a new song is played on the server
		fillContentFromStatus(data);
		getQueue();
		poll();  // Start function again
	});
}

function getUrl(subdomain) {
	//return "https://rickert.noip.me" + subdomain;  // For public site on RPi
	return "" + subdomain;  // For localhost
}