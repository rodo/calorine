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
from django.contrib.auth.models import User
from django.test import TestCase
from calorine.caro.utils import importdir, checkid3, sigfile
from calorine.caro.utils import onair_datas
from os import path
from django.core.cache import cache


class UtilsTests(TestCase):  # pylint: disable-msg=R0904
    """
    The url view

    """
    def setUp(self):
        """
        Init
        """
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')

    def test_checkid3(self):
        """
        Good id3
        """
        first = path.join(path.dirname(__file__),
                          'samples',
                          'first',
                          'test.ogg')

        datas = checkid3(first)

        self.assertEqual(datas['genre'], 'Sample')
        self.assertEqual(datas['album'], 'Lorem')

    def test_checkid3_notag(self):
        """
        Good id3
        """
        datas = checkid3(path.join(path.dirname(__file__),
                                   'samples',
                                   'notag.ogg'))
        self.assertEqual(datas, None)

    def test_checkid3_genremissing(self):
        """
        genre id3 is missing
        """
        datas = checkid3(path.join(path.dirname(__file__),
                                   'samples',
                                   'missing-genre.ogg'))
        self.assertNotEqual(datas, None)

    def test_checkid3_albummissing(self):
        """
        album id3 is missing
        """
        datas = checkid3(path.join(path.dirname(__file__),
                                   'samples',
                                   'missing-album.ogg'))
        self.assertEqual(datas, None)

    def test_checkid3_wrongunicode(self):
        """
        album id3 is missing
        """
        alpha = unicode(u"tété")
        beta = alpha.encode('iso8859-1')
        datas = checkid3(beta)
        self.assertEqual(datas, None)

    def test_sigfile(self):
        """
        Sigfile
        """
        first = path.join(path.dirname(__file__),
                          'samples',
                          'first',
                          'test.ogg')

        datas = sigfile(first)

        self.assertEqual(datas, '4c5a7fec7bfea8b4e44188918c5b68f4c90b955e')

    def test_importdir(self):
        """
        Return an array of files path
        """
        rtpath = path.dirname(__file__)
        first = path.join(rtpath,
                          'samples')

        datas = importdir(first)

        atnd = [path.join(rtpath, 'samples', 'notagg.ogg'),
                path.join(rtpath, 'samples', 'second', 'test2.ogg'),
                path.join(rtpath, 'samples', 'first', 'test.ogg')]

        self.assertEqual(datas.sort(), atnd.sort())

    def test_importdir_notexists(self):
        """
        Return an array of files path
        """
        rtpath = path.dirname(__file__)
        first = path.join(rtpath,
                          'this_dir_does_ot_exists')

        datas = importdir(first)

        self.assertEqual(datas, [])

    def test_onair(self):
        """
        Datas are present in cache
        """
        artist = 'U2'
        title = 'All I want is you'
        album = 'Rattle and Hum'

        cache.set('onair_artist', artist)
        cache.set('onair_album', album)
        cache.set('onair_title', title)

        datas = onair_datas()

        attends = {'artist': artist,
                   'title': title,
                   'album': album}

        self.assertEqual(datas, attends)

    def test_onair_nodatas(self):
        """
        Datas are not present in cache
        """
        cache.delete('onair_artist')
        cache.delete('onair_album')
        cache.delete('onair_title')

        datas = onair_datas()

        attends = {'artist': None,
                   'title': None,
                   'album': None}

        self.assertEqual(datas, attends)
