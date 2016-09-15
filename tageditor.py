#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import lib
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

if not os.geteuid() == 0:
    sys.exit("Only root can run this script")

library = lib.get_instance()


def fix():
    print "What do you want to edit?"
    print "1. Artist name"
    print "2. Album name"
    print "3. Song name"

    ans = input("Which of the following do you want to edit? ")

    if ans == 1:
        nr_files = 0
        j = 0
        print "The following artists have been found:"
        for j, artist in enumerate(
                sorted(library.get_artists(), key=lambda a: a.get_name())):
            print str(j) + ". " + artist.get_name()
        print str(j + 1) + ". None, go back"
        i = input("Which of the following artists do you want to rename? ")
        if i == j + 1:
            ask_continue()
            return
        yesno = raw_input("Do you want to rename " +
                          sorted(library.get_artists(),
                                 key=lambda a: a.get_name())[
                              i].get_name() + "? (Y/N) ")
        if yesno == "Y" or yesno == "y":
            new_name = raw_input(
                "What do you want to be the new name of the artist? ")
            artist_obj = sorted(library.get_artists(),
                                key=lambda a: a.get_name())[i]
            songs = artist_obj.get_songs()
            for song in songs:
                audio = MP3(song.get_path(), ID3=EasyID3)
                audio["artist"] = new_name.decode('unicode-escape')
                audio.save()
                nr_files += 1
            print "Files renamed:", nr_files
        ask_continue()

    if ans == 2:
        nr_files = 0
        j = 0
        print "The following albums have been found:"
        for j, album in enumerate(
                sorted(library.get_albums(), key=lambda a: a.get_title())):
            print str(j) + ". " + album.get_title()
        print str(j + 1) + ". None, go back"
        i = input("Which of the following albums do you want to rename? ")
        if i == j + 1:
            ask_continue()
            return
        yesno = raw_input("Do you want to rename " +
                          sorted(library.get_albums(),
                                 key=lambda a: a.get_title())[
                              i].get_title() + "? (Y/N) ")
        if yesno == "Y" or yesno == "y":
            new_name = raw_input(
                "What do you want to be the new name of the album? ")
            album_obj = sorted(library.get_albums(),
                               key=lambda a: a.get_title())[i]
            songs = album_obj.get_songs()
            for song in songs:
                audio = MP3(song.get_path(), ID3=EasyID3)
                audio["album"] = new_name.decode('unicode-escape')
                audio.save()
                nr_files += 1
            print "Files renamed:", nr_files
            print "Changes will become visible next time " \
                  "you run refreshlib.py"
        ask_continue()

    if ans == 3:
        j = 0
        print "The following artists have been found:"
        for j, artist in enumerate(
                sorted(library.get_artists(), key=lambda a: a.get_name())):
            print str(j) + ". " + artist.get_name()
        print str(j + 1) + ". None, go back"
        i = input("Which of the artists made the song? ")
        if i == j + 1:
            ask_continue()
            return
        artist = sorted(library.get_artists(), key=lambda a: a.get_name())[i]

        print "The following albums have been found:"
        for j, album in enumerate(
                sorted(artist.get_albums(), key=lambda a: a.get_title())):
            print str(j) + ". " + album.get_title()
        print str(j + 1) + ". None, go back"
        i = input("In which album is the song? ")
        if i == j + 1:
            ask_continue()
            return
        album = sorted(artist.get_albums(), key=lambda a: a.get_title())[i]

        print "The following songs have been found:"
        for j, song in enumerate(
                sorted(album.get_songs(), key=lambda a: a.get_title())):
            print str(j) + ". " + song.get_title()
        print str(j + 1) + ". None, go back"
        i = input("Which song do you want to rename? ")
        if i == j + 1:
            ask_continue()
            return
        song = sorted(album.get_songs(), key=lambda a: a.get_title())[i]
        yesno = raw_input(
            "Do you want to rename " + song.get_title() + "? (Y/N) ")
        if yesno == "Y" or yesno == "y":
            new_name = raw_input(
                "What do you want to be the new name of the song? ")
            audio = MP3(song.get_path(), ID3=EasyID3)
            audio["title"] = new_name.decode('unicode-escape')
            audio.save()
            print "Song renamed"
            print "Changes will become visible next time " \
                  "you run 'refreshlib.py'"
        ask_continue()


def ask_continue():
    print ""
    cont = raw_input("Do you want to edit something else? (Y/N) ")
    if cont == "y" or cont == "Y":
        fix()
    else:
        return

def fix_property_of_song(artist, album, title):
    song = library.get_song(artist, album, title)
    print song.get_title()
    audio = MP3(song.get_path(), ID3=EasyID3)

    new_name = u'El Mañana'
    audio["title"] = new_name
    audio.save()


# tag: ["title", "artist", "album", "tracknumber"]:
# audio.info.length

if __name__ == '__main__':
    print "### Tag Editor v2.0 ###"
    #fix()
    fix_property_of_song("Gorillaz", "Demon Days", "El Manana")
