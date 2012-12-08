#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, syslog, time
from optparse import OptionParser
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


def main():
    #(binary, opts) = readopts(cmdarg)

    conf = "dbname=radio user=rodo password=rodo host=localhost port=5432"
    counter = 0
    nbt = Song(conf)
    return nbt.next()

if __name__ == "__main__":
    print main()
