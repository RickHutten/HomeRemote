

function getAlbumTile(artist, album) {
	return '<div class="tile-container"><div class="tile"><image class="tile-image" src="http://rickert.noip.me/image/' + replaceAll(artist, " ", "_") + '/' + replaceAll(album, " ", "_") + '"><p>' + album + '</p><p>' + artist + '</p></div></div>'
}

function getArtistTile(artist) {
	return '<div class="tile-container"><div class="tile"><image class="tile-image" src="http://rickert.noip.me/image/' + replaceAll(artist, " ", "_") + '"><p>' + artist + '</p></div></div>'
}


function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}
