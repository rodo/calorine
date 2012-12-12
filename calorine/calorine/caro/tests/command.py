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
Unit tests for Vote

"""
from django.contrib.auth.models import User
from django.test import TestCase
from calorine.caro.models import Song
from calorine.caro.models import PlaylistEntry
from django.core.management import call_command
from datetime import datetime
from django.utils.timezone import utc


class CommandTests(TestCase):  # pylint: disable-msg=R0904
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

    def test_cleansongs(self):
        """
        cleansongs manage command
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=-1000,
                                   family=0,
                                   global_score=0)

        before = Song.objects.filter(score=-1000).count()

        call_command('cleansongs')

        after = Song.objects.filter(score=-1000).count()

        self.assertTrue(before > 0)
        self.assertEqual(after, 0)

    def test_emptyplaylist(self):
        """
        cleansongs manage command
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=-1000,
                                   family=0,
                                   global_score=0)

        ple = PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=0)


        before = PlaylistEntry.objects.all().count()

        call_command('empty_playlist')

        after = PlaylistEntry.objects.all().count()

        self.assertTrue(before > 0)
        self.assertEqual(after, 0)
