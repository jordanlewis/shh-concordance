shh-concordance
===============

Concordance for the Shenandoah Harmony

Right now it's just a little script that tries its best to extract lyrics from
a Lilypond file using lyricmode. You'll need to supply your own Lilypond files.

Usage instructions:

./extract.py [file.ly ...]

This will try to scrape lyrics from all of the provided files. It will print
out a JSON object that maps filename to list of extracted lyrics for that file.

That's it, for now!
