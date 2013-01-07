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
Unit tests for Vote

"""
from os import path
from os import unlink
from os import rmdir
from os import listdir
from tempfile import mkdtemp
from django.conf import settings
from django.test import TestCase
from calorine.caro.models import Upload
from calorine.caro.converters import convert_mp4
from calorine.caro.utils import move_file


class ConvertersTests(TestCase):  # pylint: disable-msg=R0904
    """
    The profile view

    """
    def setUp(self):
        """
        Init
        """
        settings.REMOVE_UPLOAD_FILES = False
        self.tpath = mkdtemp(prefix='calorine-test_')
        settings.UPLOAD_DEST_DIR = self.tpath

    def tearDown(self):
        """
        Clean after test
        """
        for fpath in listdir(self.tpath):
            unlink(path.join(self.tpath, fpath))
        rmdir(self.tpath)

    def test_convert_mp4(self):
        """Convert mp4 in ogg
        """
        fpath = path.join(path.dirname(__file__),
                          'samples',
                          'test.m4a')

        newpath = move_file(fpath, 'test.m4a')

        upl = Upload.objects.create(uuid='123456789',
                                    path=newpath,
                                    filename='Cocaine.mp3',
                                    content_type='audio/mp3')

        oggpath = convert_mp4(newpath, upl)

        self.assertTrue(path.exists(oggpath))
        self.assertEqual(upl.status, 'uploaded')
