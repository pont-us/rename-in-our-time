rename-in-our-time
==================

Rename MP3S of the BBC *In Our Time* programme using data from
the RSS feed.

Rationale
---------

The BBC offers MP3 downloads of Melvyn Bragg's radio programme
*In Our Time*. However, the filenames of the MP3s are not very
informative. I like my MP3s named using the following format:

`iot-150702-frederick-the-great.mp3`

That is: "iot", six-character date, title. Unfortunately the date
is not recorded in the file's own metadata, so it must be taken
from the RSS feed.

`rename-in-our-time` automatically renames *In Our Time* MP3s
according to this scheme, using the RSS feed to provide the metadata.

Usage
-----

    rename-in-our-time.py [-h] [--rssurl url] [--rssfile filename] [--test]
                                 filename [filename ...]
    
    positional arguments:
      filename            file to rename
    
    optional arguments:
      -h, --help          show a help message and exit
      --rssurl url        URL for RSS feed (default: http://www.bbc.co.uk/programmes/b006qykl/episodes/downloads.rss)
      --rssfile filename  RSS file (overrides URL)
      --test              don't actually rename; just print what would be done

License
-------

rename-in-our-time is Copyright 2016 Pontus Lurcock (pont at talvi dot
net) and released under the MIT license. The license text is included in
the source code.
