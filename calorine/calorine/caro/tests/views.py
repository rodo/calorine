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
from calorine.caro.models import Song
from calorine.caro.models import Vote
from calorine.caro.models import PlaylistEntry
from django.core.management import call_command
from calorine.caro.utils import clean_cache


class ViewsTests(TestCase):  # pylint: disable-msg=R0904
    """
    The url view

    """
    def setUp(self):  # pylint: disable-msg=C0103
        """
        Init
        """
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')

    def test_nvp_with_vote(self):
        """
        Songs never played with one vote
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')

        response = client.get('/playlist/add/%d' % song.id)

        response = client.get('/songs/never-played/')
        self.assertContains(response, song.title, status_code=200)
