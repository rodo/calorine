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
Unit tests for Song

"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from calorine.caro.models import Song
from calorine.caro.models import Vote
from datetime import date


class SongTests(TestCase):  # pylint: disable-msg=R0904
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

    def test_create_song(self):
        """
        View owner songs
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        self.assertGreater(song.id, 0)

    def test_create_song_emptytitle(self):
        """
        Create a song with empty title
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        self.assertGreater(song.id, 0)
        self.assertEqual(song.title, '')

    def test_create_song_emptyartist(self):
        """
        Create a song with empty artist
        """
        song = Song.objects.create(album='The Healing Game',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        self.assertGreater(song.id, 0)
        self.assertEqual(song.artist, '')

    def test_jingles(self):
        """
        Jingles must not be shown in /songs/
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   family=0,
                                   global_score=0)

        jingle = Song.objects.create(artist='Lino Ventura',
                                     album='Les tontons flingueurs',
                                     title='Les mecs de 100 kilos',
                                     genre='Film',
                                     score=0,
                                     family=1,
                                     global_score=0)

        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/songs/')
        self.assertContains(response, song.album, status_code=200)
        self.assertNotContains(response, jingle.album, status_code=200)

    def test_playlistEntry_unicode(self):
        """
        Check the unicode() function
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        self.assertEqual("{}".format(song), song.title)

    def test_cover(self):
        """
        Check default cover
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        self.assertEqual(song.cover, '')

    def test_userlike(self):
        """
        A user like the song, the global score increase by one
        """
        Vote.objects.all().delete()
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        result = song.userlike(self.user)

        self.assertEqual(song.global_score, 1)
        self.assertEqual(result, 0)

    def test_userlike_antispam(self):
        """
        A user like the song, the global score increase by one
        """
        Vote.objects.all().delete()
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        song.userlike(self.user)
        # we call twice like a spammer
        result = song.userlike(self.user)

        self.assertEqual(song.global_score, 1)
        self.assertEqual(result, 1)

    def test_userlike_antispam2(self):
        """
        Two user like the same song
        """
        Vote.objects.all().delete()

        userb = User.objects.create_user('adminb',
                                         'adminb@bar.com',
                                         'adminb')

        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=0)

        song.userlike(userb)
        result = song.userlike(self.user)

        self.assertEqual(song.global_score, 2)
        self.assertEqual(result, 0)

    def test_userlike_oldvote(self):
        """
        A user like the song, the global score increase by one
        """
        Vote.objects.all().delete()

        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   global_score=1)

        # the date_vote is more than 24 hours
        vote = Vote.objects.create(user=self.user,
                                   vote=1,
                                   song=song)

        vote.date_vote = date(2012, 1, 2)
        vote.save()

        result = song.userlike(self.user)

        self.assertEqual(result, 0)
        self.assertEqual(song.global_score, 2)
