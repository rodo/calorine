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
from django.test import TestCase, Client
from django.core.cache import cache
from datetime import datetime
from django.utils.timezone import utc
from calorine.caro.models import Song
from calorine.caro.models import PlaylistEntry


class UrlsTests(TestCase):  # pylint: disable-msg=R0904
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

    def test_history(self):
        """
        History url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/history/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_songs(self):
        """
        Songs url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/songs/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_main(self):
        """
        Songs url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_logs(self):
        """
        logs url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/logs/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_profile(self):
        """
        History url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/accounts/profile/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_onair(self):
        """
        History url
        """
        cache.set('onair_artist', 'footist')

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/onair.json')
        self.assertContains(response, 'footist', status_code=200)

    def test_playlistadd(self):
        """
        History url
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   family=0,
                                   global_score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/playlist/add/%d' % song.id)
        self.assertContains(response, 'ok', status_code=200)

    def test_search(self):
        """
        Search a song by title
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   family=0,
                                   global_score=0)
        song.save()

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/songs/?q=van')
        self.assertContains(response, song.artist, status_code=200)

    def test_playlist_inc(self):
        """
        Positive vote in playlist
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   family=0,
                                   global_score=0)

        ple = PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/playlist/inc/%d' % ple.id)

        self.assertContains(response, '{', status_code=200)

    def test_playlist_dec(self):
        """
        Negative vote in playlist
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   family=0,
                                   global_score=0)

        ple = PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/playlist/dec/%d' % ple.id)

        self.assertContains(response, '{', status_code=200)
