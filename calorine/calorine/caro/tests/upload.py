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
Unit tests for Upload

"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from calorine.caro.models import Upload
import os


class UploadTests(TestCase):  # pylint: disable-msg=R0904
    """
    The upload object

    """
    def setUp(self):
        """
        Init
        """
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')

    def test_create_upload(self):
        """
        View owner playlistEntrys
        """
        upl = Upload.objects.create(uuid='123456789',
                                    path='Cocaine.mp3',
                                    filename='Cocaine.mp3',
                                    content_type='audio/mp3')

        self.assertGreater(upl.id, 0)
        self.assertEqual(upl.status, u'starting')

    def test_unicode(self):
        """
        Check the unicode() function
        """
        upl = Upload.objects.create(uuid='123456789',
                                    path='Cocaine.mp3',
                                    filename='Cocaine.mp3',
                                    content_type='audio/mp3')

        self.assertEqual("{}".format(upl), upl.filename)
