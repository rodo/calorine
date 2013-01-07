# -*- coding: utf-8 -*-
#
# Copyright (c) 2012,2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
Unit tests for urls in caro

"""
from django.test import TestCase
from django.conf import settings
from calorine.caro.models import Song
from calorine.caro.models import Upload
from calorine.caro.utils import move_file
from calorine.caro.tasks import addgenre
from calorine.caro.tasks import import_upload
from calorine.caro.tasks import store_upload
from calorine.caro.tasks import get_upload_status
from uuid import uuid4
import os
import SimpleHTTPServer
import SocketServer
import threading
from pprint import pprint


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
        self.port = 10042
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer(("", self.port), JsonHandler)

    def run(self):
        print "serving at port", self.port
        # serve only one request
        self.httpd.handle_request()

    def stop(self):
        self.httpd.shutdown


class TasksTests(TestCase):  # pylint: disable-msg=R0904
    """
    TemplateTags

    """
    def setUp(self):
        """Configure env for tests
        """
        settings.REMOVE_UPLOAD_FILES = False
        settings.UPLOAD_DEST_DIR = '/tmp/'


    def test_getuploadstatus(self):
        """
        Function : get_upload_status()
        """
        http = TestServer()
        http.start()
        url = 'http://127.0.0.1:%d/progress-url-test' % (http.port)

        datas = get_upload_status("fakeuuid", url)

        self.assertEqual(datas['state'], 'done')
        http.stop()

    def test_addgenre(self):
        """Add genre
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0,
                                   cover='htt://foo.bar/img.png')

        result = addgenre(song)

        self.assertEqual(result, 0)

    def test_addgenre(self):
        """Add genre with undefined song
        """
        song = None

        result = addgenre(song)

        self.assertEqual(result, 1)

    def test_store_upload(self):
        """
        Test with a picture with cover
        """
        Upload.objects.all().delete()

        tdir = os.path.join('/tmp', str(uuid4()))
        os.mkdir(tdir)
        settings.REMOVE_UPLOAD_FILES = False
        settings.UPLOAD_DEST_DIR = tdir

        fpath = os.path.join(os.path.dirname(__file__),
                             'samples',
                             'first',
                             'test.ogg')

        move_file(fpath, 'toto.ogg')

        upl = Upload.objects.create(uuid='123456789',
                                    path=os.path.join(tdir, 'toto.ogg'),
                                    filename='The Healing Game.ogg',
                                    content_type='video/ogg')

        result = store_upload(upl)

        self.assertEqual(result, 0)
        # cleaning
        os.unlink(upl.path)
        os.unlink(os.path.join(tdir, upl.filename))
        os.rmdir(tdir)

    def test_store_upload_nonaudio(self):
        """
        Test with a picture with cover
        """
        tdir = os.path.join('/tmp', str(uuid4()))
        os.mkdir(tdir)

        settings.REMOVE_UPLOAD_FILES = False
        settings.UPLOAD_DEST_DIR = tdir

        fpath = os.path.join(os.path.dirname(__file__),
                             'samples',
                             'first',
                             'test.ogg')

        move_file(fpath, 'toto.ogg')

        upl = Upload.objects.create(uuid='123456789',
                                    path=os.path.join(tdir, 'toto.ogg'),
                                    filename='The Healing Game.ogg',
                                    content_type='image/jpeg')

        result = store_upload(upl)

        self.assertEqual(result, 1)

        # cleaning
        os.unlink(upl.path)
        os.unlink(os.path.join(tdir, upl.filename))
        os.rmdir(tdir)

    def test_store_upload_mp3(self):
        """
        Test with a picture with cover
        """
        tdir = os.path.join('/tmp', str(uuid4()))
        os.mkdir(tdir)

        settings.REMOVE_UPLOAD_FILES = False
        settings.UPLOAD_DEST_DIR = tdir

        fpath = os.path.join(os.path.dirname(__file__),
                             'samples',
                             'Cocaine.mp3')

        move_file(fpath, 'Cocaine.mp3')

        upl = Upload.objects.create(uuid='123456789',
                                    path=os.path.join(tdir, 'Cocaine.mp3'),
                                    filename='Cocaine.mp3',
                                    content_type='audio/mp3')
        self.assertEqual(store_upload(upl), 0)
        # cleaning
        os.unlink(os.path.join(tdir, 'Cocaine.ogg'))
        os.rmdir(tdir)

    def test_store_upload_wrongfile(self):
        """
        Test with a wrong file, text.mp3 contains plaintext
        """
        tdir = os.path.join('/tmp', str(uuid4()))
        os.mkdir(tdir)

        settings.REMOVE_UPLOAD_FILES = False
        settings.UPLOAD_DEST_DIR = tdir

        fpath = os.path.join(os.path.dirname(__file__),
                             'samples',
                             'text.mp3')

        move_file(fpath, 'text.mp3')

        upl = Upload.objects.create(uuid='123456789',
                                    path=os.path.join(tdir, 'text.mp3'),
                                    filename='text.mp3',
                                    content_type='audio/mp3')
        self.assertEqual(store_upload(upl), 2)
        # cleaning
        os.unlink(upl.path)
        os.rmdir(tdir)

    def test_import_upload(self):
        """
        Simple upload
        """
        Upload.objects.all().delete()
        upl = Upload.objects.create(uuid='123456789',
                                    path='/tmp/123456789',
                                    filename='The Healing Game.ogg',
                                    content_type='application/ogg')

        result = import_upload(upl.uuid, 2)

        self.assertEqual(result['state'], 'starting')

