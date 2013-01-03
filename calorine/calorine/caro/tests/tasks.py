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
from uuid import uuid4
import os


class TasksTests(TestCase):  # pylint: disable-msg=R0904
    """
    TemplateTags

    """
    def setUp(self):
        """Configure env for tests
        """
        settings.REMOVE_UPLOAD_FILES = False
        settings.UPLOAD_DEST_DIR = '/tmp/'

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

        result = addgenre.delay(song)

        self.assertTrue(result.task_id > 0)

    def test_import_upload(self):
        """
        Test with a picture with cover
        """
        Upload.objects.all().delete()
        upl = Upload.objects.create(uuid='123456789',
                                    path='/tmp/123456789',
                                    filename='The Healing Game.ogg',
                                    content_type='application/ogg')

        result = import_upload.delay(upl.uuid)

        self.assertTrue(result.task_id > 0)

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
