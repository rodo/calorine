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
Very simple client to test ircbot
"""
import socket
import os, os.path
import syslog 

def trigger(socket_fname=None):

    if socket_fname is None:
        socket_fname = "/tmp/calorine.socket"

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
                client.send("foobar")
            except:
                syslog.syslog("can't send data on  %s " % socket_fname)
        client.close()
    else:
        syslog.syslog("socket does not exists %s " % socket_fname)

