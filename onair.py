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

- python-memcache

"""
import memcache

class onair():

    def __init__(self):
        """Class initialization"""
        self.memcache_conn()

    def memcache_conn(self):
        """
        Connect to memcache
        """
        self.memcache = memcache.Client(['127.0.0.1:11211'], debug=0)

    def onair(self):
        """
        Store the actual playing song
        """
        print "Titre : %s" % self.memcache.get("onair_title")
        print "Artist : %s" % self.memcache.get("onair_artist")
        print "Full : %s " % self.memcache.get("onair_full")
        print "Score : %s " % self.memcache.get("onair_score")

if __name__ == "__main__":
    onair = onair()
    onair.onair()
