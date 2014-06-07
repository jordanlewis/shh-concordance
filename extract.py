#!/usr/bin/python

from contextlib import closing
import re
import fileinput
import json
import sys
from pyparsing import nestedExpr

# don't want these words in results
stopwords = ["tenor", "bass", "treble", "alto", ".ly", ".|.", "_",
             '\\set', 'stanza', '=', "LyricText", "StanzaNumber",
             '"D.S."']

# match stuff in quotes
quoteregex = re.compile(r'"((?:[^"\\]|\\.)*)"')
# match verse text like "2. "
verseregex = re.compile(r'"?\d\. ?"?')
# match inter-syllable dashes
dashregex = re.compile(r' -{1,2} ')

def actual_text(match):
    return match and not any(k in match for k in stopwords)

# This doesn't work very well, it just finds all the things in quotes and
# cleans them up. It misses lyricmode because those aren't quoted.
def parse_strings_simple():
    for line in fileinput.input():
        phrases = []
        for match in quoteregex.findall(line):
            match = match.strip()
            match = verseregex.sub("", match)
            match = dashregex.sub("", match)

            if not actual_text(match):
                continue
            phrases.append(match)
        if phrases:
            print fileinput.filename() + ": " + " ".join(phrases)

# Walk the tree of nested braces, searching for lyricmode content.
# Is a generator, each returned item is a list of lyrics in a lyricmode
# stanza.
def getLyricsSubtrees(tree):
    if not tree or not type(tree) == list:
        return
    nextIsLyrics = False
    for elt in tree:
        if elt == '\\lyricmode':
            # next element is our lyrics
            nextIsLyrics = True
        elif nextIsLyrics:
            nextIsLyrics = False
            yield elt
        else:
            # recurse, yield all results
            for result in getLyricsSubtrees(elt):
                yield result


# a valid word inside of lyricsmode stanzas. have to skip various control
# structures, stopwords and verse markers
def valid_word(word):
    return word not in stopwords \
           and not verseregex.match(word) \
           and not word.startswith('\\') \
           and not word.startswith('#')

def main():
    if len(sys.argv) <= 2:
        print "usage: ./extract.py tunefile.ly [tunefile2.ly, ...]"
        sys.exit(1)
    res = {}
    for filename in sys.argv[1:]:
        with closing(open(filename)) as file:
            lines = [line.replace("%", "") for line in file]
            tree = nestedExpr("{", "}", None, None).parseString(
                                "{%s}" % " ".join(lines)).asList()
            blocks = []
            for subtree in getLyricsSubtrees(tree):
                subtree = [w for w in subtree if valid_word(w)]
                block = " ".join(subtree)
                block = dashregex.sub("", block)
                if block:
                    blocks.append(block)
            res[filename] = list(set(blocks))

    print json.dumps(res, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
