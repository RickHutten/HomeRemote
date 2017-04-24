function getAlbumTile(artist, album) {
	return '<div class="tile-container"><div class="tile album-tile" onclick="onAlbumClicked(this)"><image class="tile-image" src="' + getUrl('/image/' + replaceAll(artist, " ", "_") + '/' + replaceAll(album, " ", "_")) + '"><p>' + album + '</p><p>' + artist + '</p></div></div>'
}

function getArtistTile(artist) {
	return '<div class="tile-container"><div class="tile artist-tile"><image class="tile-image" src="' + getUrl('/image/' + replaceAll(artist, " ", "_")) + '"><p>' + artist + '</p></div></div>'
}

function getAlbumView(artist, album, songs) {
	var basehtml = '<div class="album-header"><image class="album-view-image" src="' + getUrl('/image/' + replaceAll(artist, " ", "_") + '/' + replaceAll(album, " ", "_")) + '"><div class="album-text-container"><h1><p class="center-text" id="album">' + album + '</p></h1><p class="center-text" id="artist">' + artist + '</p></div></div><div class="song-container">';
	var endhtml = '</div>';

	var songhtml = '';
	for (i = 0; i < songs.length; i++) {
		var song = songs[i];
		var title = song.title;
		var duration = Math.floor(song.duration);
		var seconds = duration % 60;
		var minutes = Math.floor(duration / 60);
		duration = "" + minutes + ":";
		if (seconds < 10) {
			duration += "0";
		}
		duration += seconds;
		
		if (i == songs.length - 1) {
			songhtml += getSongView(artist, album, title, duration, false);
		} else {
			songhtml += getSongView(artist, album, title, duration, true);
		}
	}
	return basehtml + songhtml + endhtml;
	
}

function getQueueSongs(queue) {
	str = "";
	if (queue == null) {
		return str;
	}
	for (i = 0; i < queue.length; i++) {
		var song = queue[i];
		var artist = song.artist;
		var album = song.album;
		var title = song.song;
		var duration = Math.floor(song.duration);
		var seconds = duration % 60;
		var minutes = Math.floor(duration / 60);
		duration = "" + minutes + ":";
		if (seconds < 10) {
			duration += "0";
		}
		duration += seconds;
		
		if (i == queue.length - 1) {
			str += getQueueSongView(artist, album, title, duration, false);
		} else {
			str += getQueueSongView(artist, album, title, duration, true);
		}
	}
	return str;
}

function getQueueSongView(artist, album, title, duration, border_bottom) {
	if (border_bottom) {
		return '<div class="queue-song-view border-bottom" onclick="onSongClicked(this)" artist="'+artist+'" album="'+album+'" title="'+title+'"><p class="queue-song-title">'+title+'</p><p class="queue-song-duration">'+duration+'</p></div>';
	}
	return '<div class="queue-song-view" onclick="onSongClicked(this)" artist="'+artist+'" album="'+album+'" title="'+title+'"><p class="queue-song-title">'+title+'</p><p class="queue-song-duration">'+duration+'</p></div>';
}


function getSongView(artist, album, title, duration, border_bottom) {
	if (border_bottom) {
		return '<div class="song-view border-bottom" onclick="onSongClicked(this)" artist="'+artist+'" album="'+album+'" title="'+title+'"><p class="song-title">'+title+'</p><p class="song-duration">'+duration+'</p></div>';
	}
	return '<div class="song-view" onclick="onSongClicked(this)" artist="'+artist+'" album="'+album+'" title="'+title+'"><p class="song-title">'+title+'</p><p class="song-duration">'+duration+'</p></div>';
}

function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}
