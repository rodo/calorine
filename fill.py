#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import os, syslog, time
from stat import ST_MTIME
import psycopg2
import mutagen
from song import Song

def readopts(cmdargs):
    """
    Read options passed on command line
    """
    opts = ""
    parser = OptionParser()
    parser.add_option("--exclude-list-file",
                      action="store",
                      type="string",
                      dest="exclude_filelist",
                      default=None)

    parser.add_option("--binary",
                      action="store",
                      type="string",
                      dest="clocpath",
                      default="/usr/bin/cloc")

    options = parser.parse_args(args=cmdargs)[0]

    if options.exclude_filelist is not None:
        opts = load_exclude(options.exclude_filelist)

    if options.clocpath is not None:
        if not path.isfile(options.clocpath):
            exit('File does not exists : %s' % (options.clocpath))
        if not access(options.clocpath, X_OK):
            exit('File does not exists : %s' % (options.clocpath))
    return options.clocpath, opts

def importdir(path, counter, conf):

    extensions = ['ogg', 'mp3']
    nbt = Song(conf)
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path,filename.strip())):
            importdir(os.path.join(path,filename.strip()), counter, conf)
        else:
            ext = filename.split('.')[-1]
            if ext in extensions:
                nbt.newsong(os.path.join(path,filename.strip()))
                print counter, filename.strip()
                counter += 1
    return counter

def main():

    conf = "dbname=devradio"

    counter = 0

    path = "/home/Music/AATrier"

    importdir(path, counter, conf)

if __name__ == "__main__":
    main()


