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
                    mp3ogg(fullname)


    return counter

def mp3ogg(fname):

    mpg = subprocess.Popen(["/usr/bin/mpg123",
                            fname,
                            "-w",
                            "-"], stdout=subprocess.PIPE)
    
    ogg = subprocess.Popen(["/usr/bin/oggenc",
                            "-o",
                            "%s.ogg" % fname[:-4],
                            "-"],
                           stdin=mpg.stdout, stdout=subprocess.PIPE)
    output = ogg.communicate()[0]


def main():
    """
    Main function
    """
    if len(sys.argv) == 1:
        print "Usage convert.py DIRNAME"
        sys.exit(1)
    path = sys.argv[-1]

    if not os.path.isdir(path):
        print "%s does not exists" % path

    importdir(path)

if __name__ == "__main__":
    main()
