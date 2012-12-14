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
Unit tests for PlaylistEntry

"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import Song
from datetime import datetime
from django.utils.timezone import utc


class PlaylistEntryTests(TestCase):  # pylint: disable-msg=R0904
    """
    The profile view

    """
    def setUp(self):
        """
        Init
        """
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')

    def test_create_playlistEntry(self):
        """
        View owner playlistEntrys
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        ple = PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=0)

        self.assertGreater(ple.id, 0)

    def test_playlistEntry_getnonempty(self):
        """
        Check playlist page display right information
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        ple = PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/')
        self.assertContains(response, song.artist, status_code=200)
        self.assertContains(response, song.album, status_code=200)
        self.assertContains(response, song.title, status_code=200)

    def test_playlistEntry_unicode(self):
        """
        Check the unicode() function
        """
        song = Song.objects.create(artist='The Fugees',
                                   album='The Score',
                                   title='Cowboys',
                                   genre='Funk',
                                   score=0,
                                   global_score=0)

        ple = PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=0)

        self.assertEqual("{}".format(ple), song.title)
