shh-concordance
===============

Concordance for the Shenandoah Harmony

Right now it's just a little script that tries its best to extract lyrics from
Lilypond files that use lyricmode for lyrics. You'll need to supply your own
Lilypond files if you want to try it out.

Usage instructions:

./extract.py [file.ly ...]

This will try to scrape lyrics from all of the provided files. It will print
out a JSON object that maps filename to list of extracted lyrics for that file.

That's it, for now!
