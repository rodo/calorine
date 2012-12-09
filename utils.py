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

import socket
import os, os.path
import syslog 
import hashlib
import mutagen

def strtag(fname):
    """Return a string based on ID3 tags
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
    return "%s - %s" % (datas['artist'], datas['title'])

def trigger(fname, socket_fname=None):

    if socket_fname is None:
        socket_fname = "/tmp/python_unix_sockets_example"

    connected = False

    if os.path.exists(socket_fname):
        client = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )

        try:
            client.connect(socket_fname)
            connected = True
        except socket.error:
            syslog.syslog("Couldn't Connect to %s " % socket_fname)
            
        if connected:
            try:
                client.send( "On AIR : %s" % strtag(fname))
            except:
                syslog.syslog("can't send data on  %s " % socket_fname)
        client.close()
    else:
        syslog.syslog("socket does not exists %s " % socket_fname)


def hashfile(filepath):
    """
    Calculate the sha1 value of a file
    """
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()
