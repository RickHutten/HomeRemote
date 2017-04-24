

function getAlbumTile(artist, album) {
	return '<div class="tile-container"><div class="tile album-tile" onclick="onAlbumClicked(this)"><image class="tile-image" src="' + getUrl('/image/' + replaceAll(artist, " ", "_") + '/' + replaceAll(album, " ", "_")) + '"><p>' + album + '</p><p>' + artist + '</p></div></div>'
}

function getArtistTile(artist) {
	return '<div class="tile-container"><div class="tile artist-tile"><image class="tile-image" src="' + getUrl('/image/' + replaceAll(artist, " ", "_")) + '"><p>' + artist + '</p></div></div>'
}

function getAlbumView(artist, album, songs) {
	var basehtml = '<div class="album-header"><div class="album-view-image-container"><image class="album-view-image" src="' + getUrl('/image/' + replaceAll(artist, " ", "_") + '/' + replaceAll(album, " ", "_")) + '"></div><div class="album-text-container"><h1><p class="center-text" id="album">' + album + '</p></h1><p class="center-text" id="artist">' + artist + '</p></div></div><div class="song-container">';
	var endhtml = '</div>';

	var songhtml = '';
	for (i = 0; i < songs.length; i++) {
		var song = songs[i];
		var title = song.title;
		var duration = song.duration;
		songhtml += '<div class="song-view" onclick="onSongClicked(this)" artist="'+artist+'" album="'+album+'" title="'+title+'"><p class="song-title">'+title+'</p><p class="song-duration">'+Math.floor(duration)+'</p></div>';
	}
	return basehtml + songhtml + endhtml;
	
}

function getSongView(artist, album, title, duration) {
	
}

function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}
