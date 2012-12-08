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
from song import Song

def importdir(path, counter):
    """
    Import all files present in dir recursively
    """
    extensions = ['ogg', 'mp3']
    nbt = Song()
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename.strip())):
            importdir(os.path.join(path, filename.strip()), counter)
        else:
            ext = filename.split('.')[-1]
            if ext in extensions:
                nbt.newsong(os.path.join(path, filename.strip()))
                print counter, filename.strip()
                counter += 1
    return counter

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
