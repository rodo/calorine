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
Unit tests for profil in caro

"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.core.cache import cache
import memcache
from calorine.caro.models import Song
from calorine.caro.models import PlaylistEntry


class CachesTests(TestCase):  # pylint: disable-msg=R0904
    """
    The logs object

    """
    def setUp(self):  # pylint: disable-msg=C0103
        """
        Init
        """
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')

    def test_cache(self):
        """Debug cache use
        """
        key = "onair_title_foo"
        value = "from"
        prefix = settings.CACHES['default']['KEY_PREFIX']

        mmc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mmc.set("%s:1:%s" % (prefix, key), value)

        self.assertEqual(cache.get(key), value)

    def test_voteafteradd(self):
        """
        After adding a song 2 keys must be present in cache
        """
        prefix = settings.CACHES['default']['KEY_PREFIX']
        PlaylistEntry.objects.all().delete()
        song = Song.objects.create(artist='Alexis HK',
                                   album='Belleville',
                                   title='Diable attend',
                                   genre=u'''Chanson française''',
                                   score=0,
                                   family=0,
                                   global_score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')
        client.get('/playlist/add/%d' % song.id)

        ple = PlaylistEntry.objects.all()[0]

        key = 'ple_{}_{}'.format(self.user.id, ple.pk)
        song_key = 'song_{}'.format(ple.song.pk)

        mmc = memcache.Client(['127.0.0.1:11211'], debug=0)

        value = mmc.get("%s:1:%s" % (prefix, key))
        song_value = mmc.get("%s:1:%s" % (prefix, song_key))

        self.assertEqual(value, True)
        self.assertEqual(song_value, True)
