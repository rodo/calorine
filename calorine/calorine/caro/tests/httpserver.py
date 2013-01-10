# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
Basic httpserver usefull for testing

"""
import SimpleHTTPServer
import SocketServer
import threading


class JsonHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Basic handler, serve a basic JSON answer
    """
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('{"state": "done"}')


class TestServer(threading.Thread):
    """
    Basic http server to serve JSON
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = 1024
        connected = False
        while not connected and self.port < 2048:
            try:
                self.httpd = SocketServer.TCPServer(("", self.port),
                                                    JsonHandler)
                self.httpd.timeout = 30
                connected = True
            except:
                self.port = self.port + 1

    def run(self):
        print "serving at port", self.port
        self.httpd.handle_request()


class LastFMHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Basic handler, serve a basic JSON answer
    """
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('{"state": "done"}')


class LastFMServer(threading.Thread):
    """
    Basic http server to serve JSON
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = 1024
        connected = False
        while not connected and self.port < 2048:
            try:
                self.httpd = SocketServer.TCPServer(("", self.port),
                                                    LastFM)
                self.httpd.timeout = 30
                connected = True
            except:
                self.port = self.port + 1

    def run(self):
        print "serving at port", self.port
        self.httpd.handle_request()
