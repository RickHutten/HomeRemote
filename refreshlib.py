#!/usr/bin/env python
import lib.scrape
import lib.tagfix

ans = raw_input(
    "Would you like to check your music library for errors? (Y/N) ")
while ans != "n" and ans != "N" and ans != "y" and ans != "Y":
    print "Could not understand answer"
    ans = raw_input(
        "Would you like to check your music library for errors? (Y/N) ")
if ans == "Y" or ans == "y":
    lib.tagfix.fix()

lib.scrape.scrape()
