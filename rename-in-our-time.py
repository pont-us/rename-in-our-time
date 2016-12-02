#!/usr/bin/env python3

# rename-in-our-time is Copyright 2016 Pontus Lurcock (pont at talvi dot
# net) and released under the MIT license.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import xml.etree.ElementTree
from datetime import datetime
import os
import os.path
from unidecode import unidecode
import argparse
import urllib.request

def makemap(xml_file):
    "Return a map from original filename to descriptive filename"

    root = xml.etree.ElementTree.parse(xml_file).getroot()

    date_fmt = "%a, %d %b %Y %H:%M:%S %z"
    illegal_chars = r"`~!@#$%^&*()|\[]{}'\";:/?.,<>"
    trans_tab = str.maketrans(" ", "-", illegal_chars)

    items = [i for i in root[0] if i.tag == "item"]
    name_map = {}

    for item in items:
        
        def get(tag):
            return item.find(tag).text

        title = get("title")
        pubdate = datetime.strptime(get("pubDate"), date_fmt)
        datestr = datetime.strftime(pubdate, "%y%m%d")
        filename = os.path.basename(item.find("enclosure").get("url"))
        desc = get("description")
        newname = "iot-%s-%s.mp3" % \
                  (datestr,
                   unidecode(title).lower().translate(trans_tab))
        name_map[filename] = newname

    return name_map

def main():

    parser = argparse.ArgumentParser(description="Rename In Our Time mp3s",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("filenames", metavar="filename", type=str, nargs="+",
                        help="file to rename")
    parser.add_argument("--rssurl", metavar="url", type=str, 
                        default="http://www.bbc.co.uk/programmes/b006qykl/episodes/downloads.rss",
                        help="URL for RSS feed")
    parser.add_argument("--rssfile", metavar="filename", type=str, 
                        help="RSS file (overrides URL)")
    parser.add_argument("--test", action="store_true",
                        help="don't actually rename; just print what would be done")
    args = parser.parse_args()

    if (args.rssfile):
        name_map = makemap(args.rssfile)
    else:
        filename, headers = urllib.request.urlretrieve(args.rssurl)
        name_map = makemap(filename)
        os.remove(filename)

    for filename in args.filenames:
        parent, basename = os.path.split(filename)
        if basename in name_map:
            newname = os.path.join(parent, name_map[basename])
            print(filename, "->", newname)
            if (not args.test):
                os.rename(filename, newname)
        else:
            print("*** No data for %s!" % basename)

if __name__=="__main__":
    main()
