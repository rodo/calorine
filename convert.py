#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
convert.py convert all files from mp3 to ogg recursively
"""
import os
import sys
import subprocess
import mutagen

__OGGENC__ = "/usr/bin/oggenc"
__MPG123__ = "/usr/bin/mpg123"

def importdir(path):
    """
    Import all files present in dir recursively
    """
    counter = 0
    extensions = ['mp3']
    dirlist = []
    try:
        dirlist = os.listdir(path)
    except OSError as e:
        pass

    for filename in dirlist:
        
        fullname = os.path.join(path, filename.strip())

        if os.path.isdir(os.path.join(path, filename.strip())):
            importdir(os.path.join(path, filename.strip()))
        else:
            ext = filename.split('.')[-1]
            if ext in extensions:
                if not os.path.isfile("%s.ogg" % fullname[:-4]):
                    datas = readtags(fullname)
                    mp3ogg(fullname, datas)


    return counter

def readtags(fname):
    """Read mp3 IDS Tags

    Return array with tags
    """
    datas = {}
    fields = ['album', 'artist', 'title', 'genre', 'date', 'tracknumber']
    muts = mutagen.File(fname, easy=True)
    for fld in fields:
        if not muts.has_key(fld):
            datas[fld] = ''
        else:
            data = muts[fld]
            datas[fld] = data[0]
    return datas

def mp3ogg(fname, datas):
    """
    Encode mp3 files to ogg vorbis
    """
    mpg = subprocess.Popen([__MPG123__,
                            "-w",
                            "-",
                            fname],
                           stdout=subprocess.PIPE)
    
    command = [__OGGENC__,
               "--artist", datas['artist'],
               "--title", datas['title'],
               "--album", datas['album'],
               "--genre", datas['genre'],
               "--date", datas['date'],
               "--tracknum", datas['tracknumber'],
               "-o", "%s.ogg" % fname[:-4],
               "-"]

    ogg = subprocess.Popen(command,
                           stdin=mpg.stdout, stdout=subprocess.PIPE)
    output = ogg.communicate()[0]


def main():
    """
    Main function
    """
    if not os.path.isfile(__OGGENC__):
        print "%s not found, please install vorbis tools" % __OGGENC__
        sys.exit(2)

    if not os.path.isfile(__MPG123__):
        print "%s not found, please install vorbis tools" % __MPG123__
        sys.exit(2)

    if len(sys.argv) == 1:
        print "Usage convert.py DIRNAME"
        sys.exit(1)
    path = sys.argv[-1]

    if not os.path.isdir(path):
        print "%s does not exists" % path

    importdir(path)

if __name__ == "__main__":
    main()
