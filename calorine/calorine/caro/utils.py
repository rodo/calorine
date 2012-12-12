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
fill.py is used to fill the database with music files
"""
import os
import sys
import hashlib
import mutagen

def checkID3(filename):
    """
    Create a new song in database
    """
    datas = None
    mdat = None
    try:
        unicode(filename)
    except UnicodeDecodeError:
        pass

    try:
        mdat = mutagen.File(filename, easy=True)
    except:
        pass

    if mdat is not None:
        try:
            datas = {'artist': mdat['artist'][0],
                     'album': mdat['album'][0],
                     'title': mdat['title'][0],
                     'genre': mdat['genre'][0]}
        except KeyError as e:
            msg = str(sys.exc_type), ":", "%s is not in the list." % sys.exc_value
            
    return datas

def sigfile(fpath):
    """
    Calculate the sha1 value of a file
    """
    sha1 = hashlib.sha1()
    f = open(fpath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()


def importdir(path):
    """
    Import all files present in dir recursively

    Return an array containing all paths
    """
    paths = []
    extensions = ['ogg']
    dirlist = []
    try:
        dirlist = os.listdir(path)
    except OSError as e:
        pass

    for filename in dirlist:
        if os.path.isdir(os.path.join(path, filename.strip())):
            for filex in importdir(os.path.join(path,
                                                filename.strip())):
                paths.append(filex)
        else:
            ext = filename.split('.')[-1]
            if ext in extensions:
                paths.append(os.path.join(path, filename.strip()))

    return paths

def main():
    """
    Main function
    """
    if len(sys.argv) == 1:
        print "Usage fill.py [options] --dbname=DBNAME DIRNAME"
        sys.exit(1)
    path = sys.argv[-1]

    if not os.path.isdir(path):
        print "%s does not exists" % path

    counter = 0
    importdir(path, counter)

if __name__ == "__main__":
    main()
