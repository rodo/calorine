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
    
    sample = {"track": 
              {"id":"1019817",
               "name":"Believe",
               "mbid":"64e9df18-0ffb-4fda-bac8-6b52b926c7ec",
               "url":"http:\/\/www.last.fm\/music\/Cher\/_\/Believe",
               "duration":"222000",
               "streamable":{"#text":"1","fulltrack":"0"},
               "listeners":"287841",
               "playcount":"1208728",
               "artist":{"name":"Cher",
                         "mbid":"bfcc6d75-a6a5-4bc6-8282-47aec8531818",
                         "url":"http:\/\/www.last.fm\/music\/Cher"},
               "album":{"artist":"Cher",
                        "title":"The Very Best of Cher",
                        "mbid":"5df00011-6e57-4837-99ae-61f398481db5",
                        "url":"http:\/\/www.last.fm\/music\/Cher\/The+Very+Best+of+Cher",
                        "image":[{"#text":"http:\/\/userserve-ak.last.fm\/serve\/64s\/71997588.png",
                                  "size":"small"},
                                 {"#text":"http:\/\/userserve-ak.last.fm\/serve\/126\/71997588.png",
                                  "size":"medium"},
                                 {"#text":"http:\/\/userserve-ak.last.fm\/serve\/174s\/71997588.png",
                                  "size":"large"},
                                 {"#text":"http:\/\/userserve-ak.last.fm\/serve\/300x300\/71997588.png",
                                  "size":"extralarge"}],
                        "@attr":{"position":"1"}},
               "toptags":{"tag":[{"name":"pop",
                                  "url":"http:\/\/www.last.fm\/tag\/pop"},
                                 {"name":"dance",
                                  "url":"http:\/\/www.last.fm\/tag\/dance"},
                                 {"name":"90s",
                                  "url":"http:\/\/www.last.fm\/tag\/90s"},
                                 {"name":"cher",
                                  "url":"http:\/\/www.last.fm\/tag\/cher"},
                                 {"name":"female vocalists","url":"http:\/\/www.last.fm\/tag\/female%20vocalists"}]},
               "wiki":{"published":"Tue, 17 Nov 2009 15:02:18 +0000",
                       "summary":"blah blah"}
               }
              }

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('%s' % sample)


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
                                                    LastFMHandler)
                self.httpd.timeout = 30
                connected = True
            except:
                self.port = self.port + 1

    def run(self):
        print "serving at port", self.port
        self.httpd.handle_request()
