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
from calorine.caro.models import HistoryEntry
from calorine.caro.models import UserProfile
from django.core.management import call_command
from os import path
from StringIO import StringIO


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
        Song.objects.create(artist='Van Morrison',
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
        song.add_to_playlist()

        before = PlaylistEntry.objects.all().count()

        call_command('empty_playlist')

        after = PlaylistEntry.objects.all().count()

        self.assertTrue(before > 0)
        self.assertEqual(after, 0)

    def test_importsongs(self):
        """
        importsongs
        """
        Song.objects.all().delete()
        dpath = path.join(path.dirname(__file__), 'samples')

        call_command('importsongs', dpath)

        genre = Song.objects.filter(genre='Sample').count()
        artist = Song.objects.filter(artist='Foobar').count()

        self.assertEqual(genre, 1)
        self.assertEqual(artist, 2)

    def test_importsongs_pathdoesnotexists(self):
        """
        importsongs with a non existent path on arg
        """
        Song.objects.all().delete()
        dpath = path.join(path.dirname(__file__), 'this_path_does_not_exists')

        before = Song.objects.all().count()

        call_command('importsongs', dpath)

        after = Song.objects.all().count()

        self.assertEqual(before, after)

    def test_importsongs_samefile(self):
        """
        importsongs twice to test update path

        The same file is in the twice dir
        """
        Song.objects.all().delete()
        first = path.join(path.dirname(__file__),
                          'samples',
                          'first')

        dpath = path.join(path.dirname(__file__),
                          'samples',
                          'second')

        call_command('importsongs', first)
        call_command('importsongs', dpath)

        genre = Song.objects.filter(genre='Sample').count()
        artist = Song.objects.filter(artist='Foobar').count()

        self.assertEqual(genre, 1)
        self.assertEqual(artist, 1)

    def test_importsongs_samedir(self):
        """
        importsongs twice to test update path

        The same file is in the twice dir
        """
        Song.objects.all().delete()
        first = path.join(path.dirname(__file__),
                          'samples',
                          'first')

        call_command('importsongs', first)
        call_command('importsongs', first)

        genre = Song.objects.filter(genre='Sample').count()
        artist = Song.objects.filter(artist='Foobar').count()

        self.assertEqual(genre, 1)
        self.assertEqual(artist, 1)

    def test_importsongs_missingpath(self):
        """
        importsongs twice to test update path

        Path is missing
        """
        Song.objects.all().delete()

        call_command('importsongs')

        self.assertEqual(Song.objects.all().count(), 0)

    def test_playlistrandomsong(self):
        """
        Add a random song in playlist
        """
        Song.objects.create(artist='Van Morrison',
                            album='The Healing Game',
                            title='Sometimes We Cry',
                            genre='Blues',
                            score=0,
                            family=0,
                            global_score=0)

        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Nayan',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        before = PlaylistEntry.objects.all().count()

        call_command('playlist_random_song')

        after = PlaylistEntry.objects.all().count()

        self.assertEqual(before, 0)
        self.assertTrue(after > 0)

    def test_playlistrandomsong1(self):
        """
        Add a random song in playlist, with only 1 one song present in DB
        """
        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Nayan',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        before = PlaylistEntry.objects.all().count()

        call_command('playlist_random_song')

        after = PlaylistEntry.objects.all().count()

        self.assertEqual(before, 0)
        self.assertTrue(after > 0)

    def test_playlistrandomsong_nosong(self):
        """
        Run management command 'playlist_random_song'with no song in db
        """
        Song.objects.all().delete()
        PlaylistEntry.objects.all().delete()

        call_command('playlist_random_song')

        self.assertEqual(PlaylistEntry.objects.all().count(), 0)

    def test_lookup_add_playlist(self):
        """
        Management command lookup_add_playlist

        Lookup for a song and add them in playlist if found
        """
        PlaylistEntry.objects.all().delete()

        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Nayan',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        before = PlaylistEntry.objects.all().count()

        call_command('lookup_add_playlist', 'Nayan')

        after = PlaylistEntry.objects.all().count()

        self.assertEqual(before, 0)
        self.assertEqual(after, 1)

    def test_lookup_add_playlist_twice(self):
        """
        Management command lookup_add_playlist

        Lookup for a song and add them in playlist if found
        """
        PlaylistEntry.objects.all().delete()

        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Nayan',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        call_command('lookup_add_playlist', 'Nayan')
        # call twice
        call_command('lookup_add_playlist', 'Nayan')

        self.assertEqual(PlaylistEntry.objects.all().count(), 1)

    def test_lookup_add_playlist2songsmatch(self):
        """
        Management command lookup_add_playlist

        Lookup for a song and add them in playlist if found
        """
        PlaylistEntry.objects.all().delete()

        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Nayan',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Kanou',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        before = PlaylistEntry.objects.all().count()

        call_command('lookup_add_playlist', 'Fatoumata')

        after = PlaylistEntry.objects.all().count()

        self.assertEqual(before, 0)
        self.assertEqual(after, 1)

    def test_lookupaddplaylist_missingargs(self):
        """
        Management command lookup_add_playlist

        Lookup for a song and add them in playlist if found
        """
        PlaylistEntry.objects.all().delete()

        Song.objects.create(artist='Fatoumata Diawara',
                            album='Kanou',
                            title='Nayan',
                            genre='Folk Wassoulou',
                            score=0,
                            family=0,
                            global_score=0)

        before = PlaylistEntry.objects.all().count()

        call_command('lookup_add_playlist')

        after = PlaylistEntry.objects.all().count()

        self.assertEqual(before, 0)
        self.assertEqual(after, 0)

    def test_nosongsmatch(self):
        """
        Management command lookup_add_playlist

        Lookup for a song, no song will match
        """
        PlaylistEntry.objects.all().delete()
        Song.objects.all().delete()

        Song.objects.create(artist='Lou Reed',
                            album='Transformer',
                            title='''Andy's Chest''',
                            genre='Glam rock',
                            score=0,
                            family=0,
                            global_score=0)

        before = PlaylistEntry.objects.all().count()

        call_command('lookup_add_playlist', 'Farka')

        after = PlaylistEntry.objects.all().count()

        self.assertEqual(before, 0)
        self.assertEqual(after, 0)

    def test_checkfiles(self):
        """
        Management command that check existent files or not

        """
        PlaylistEntry.objects.all().delete()
        Song.objects.all().delete()

        Song.objects.create(artist='Lou Reed',
                            album='Transformer',
                            title='''Andy's Chest''',
                            genre='Glam rock',
                            score=0,
                            family=0,
                            global_score=0,
                            filename='/tmp/file_does_not_exists')

        Song.objects.create(artist='File',
                            album='Exists',
                            title='''Andy's Chest''',
                            genre='Glam rock',
                            score=0,
                            family=0,
                            global_score=0,
                            filename=path.join(path.dirname(__file__),
                                               'samples',
                                               'notagg.ogg'))

        attend = u'/tmp/file_does_not_exists is missing\n1 songs are missing\n'

        content = StringIO()
        call_command('check_files', stdout=content)
        content.seek(0)

        self.assertEqual(content.read(), attend)

    def test_munin(self):
        """
        Management command for munin

        """
        Song.objects.all().delete()

        Song.objects.create(artist='Lou Reed',
                            album='Transformer',
                            title='''Andy's Chest''',
                            genre='Glam rock',
                            score=0,
                            family=0,
                            global_score=0,
                            filename='/tmp/this_file_does_not_exists')

        Song.objects.create(artist='The Who',
                            album='Best Of Who',
                            title='''You Better You Bet''',
                            genre='Rock',
                            score=0,
                            played=1,
                            family=0,
                            global_score=0,
                            filename='/tmp/this_file_does_not_exists')

        attend = ('\n').join(('notfound.value 0',
                             'neverplayed.value 1',
                             'playedone.value 1',
                             'playedmore.value 0',
                             'total.value 2\n'))

        content = StringIO()
        call_command('munin', stdout=content)
        content.seek(0)

        self.assertEqual(content.read(), attend)

    def test_lastfm(self):
        """
        Management command that add genre tag on song by querying lastfm API
        """
        Song.objects.all().delete()

        Song.objects.create(artist='Lou Reed',
                            album='Transformer',
                            title='''song title''',
                            genre='',
                            score=0,
                            family=0,
                            global_score=0)

        content = StringIO()
        call_command('lastfm', stdout=content)
        content.seek(0)

        attend = '1 song title\n'

        self.assertEqual(content.read(), attend)

    def test_irclike(self):
        """
        Management command irclike

        The last play song has a score increase by one
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()
        userp = UserProfile.objects.get(user=self.user)

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=0)

        HistoryEntry.objects.create(song=song)

        before = song.global_score

        content = StringIO()
        call_command('irclike', userp.ircnick, stdout=content)
        content.seek(0)

        upsong = Song.objects.get(pk=song.id)

        after = upsong.global_score

        self.assertEqual(before, 0)
        self.assertEqual(after, 1)

    def test_irclike_nonick(self):
        """
        Management command irclike

        The nick is missing, no action
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=0)

        HistoryEntry.objects.create(song=song)

        before = song.global_score

        content = StringIO()
        call_command('irclike', stderr=content)
        content.seek(0)
        output = content.read()

        upsong = Song.objects.get(pk=song.id)

        after = upsong.global_score

        self.assertEqual(before, 0)
        self.assertEqual(after, 0)
        self.assertEqual(output,
                         "Erreur, vous devez indiquez un nick irc en option")

    def test_irclike_spam(self):
        """
        Management command irclike

        The same user vote for the same song twice, it must be impossible
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()
        userp = UserProfile.objects.get(user=self.user)

        fatou = Song.objects.create(artist='Fatoumata Diawara',
                                    album='Kanou',
                                    title='Nayan',
                                    genre='Folk Wassoulou',
                                    score=0,
                                    family=0,
                                    global_score=0)

        lou = Song.objects.create(artist='Lou Reed',
                                  album='Transformer',
                                  title='''song title''',
                                  genre='',
                                  score=0,
                                  family=0,
                                  global_score=0)

        HistoryEntry.objects.create(song=lou)
        HistoryEntry.objects.create(song=fatou)

        self.assertEqual(HistoryEntry.objects.all().count(), 2)

        before = fatou.global_score

        # first like
        call_command('irclike', userp.ircnick)

        # second like
        content = StringIO()
        call_command('irclike', userp.ircnick, stdout=content)
        content.seek(0)
        output = content.read()

        after = Song.objects.get(pk=fatou.id).global_score

        self.assertEqual(before, 0)
        self.assertEqual(after, 1)
        msg = "On vote une seule fois par jour %s\n"
        self.assertEqual(output, msg % userp.ircnick)

    def test_irclike_suds(self):
        """
        Management command irclike

        The same user vote for two different songs
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()
        userp = UserProfile.objects.get(user=self.user)

        fatou = Song.objects.create(artist='Fatoumata Diawara',
                                    album='Kanou',
                                    title='Nayan',
                                    genre='Folk Wassoulou',
                                    score=0,
                                    family=0,
                                    global_score=0)

        lou = Song.objects.create(artist='Lou Reed',
                                  album='Transformer',
                                  title='''song title''',
                                  genre='',
                                  score=0,
                                  family=0,
                                  global_score=0)

        # first song
        HistoryEntry.objects.create(song=lou)
        call_command('irclike', userp.ircnick)
        self.assertEqual(Song.objects.get(pk=lou.id).global_score, 1)

        # second song
        HistoryEntry.objects.create(song=fatou)
        call_command('irclike', userp.ircnick)
        self.assertEqual(Song.objects.get(pk=fatou.id).global_score, 1)

    def test_irclike_badnick(self):
        """
        Management command irclike

        The nick is unknown
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=0)

        HistoryEntry.objects.create(song=song)

        before = song.global_score

        nick = 'this_is_not_a_real_nick'

        content = StringIO()
        call_command('irclike', nick, stderr=content)
        content.seek(0)
        output = content.read()

        upsong = Song.objects.get(pk=song.id)

        after = upsong.global_score

        self.assertEqual(before, 0)
        self.assertEqual(after, 0)
        self.assertEqual(output,
                         'nick [%s] does not exist' % nick)

    def test_ircdislike(self):
        """
        Management command ircdislike

        The last play song has a score decrease by one
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=10)

        HistoryEntry.objects.create(song=song)
        userp = UserProfile.objects.get(user=self.user)
        before = song.global_score

        content = StringIO()
        call_command('ircdislike', userp.ircnick, stdout=content)
        content.seek(0)

        self.assertEqual(before, 10)
        self.assertEqual(Song.objects.get(pk=song.id).global_score, 9)

    def test_ircdislike_spamdetection(self):
        """
        Management command ircdislike

        The last play song has a score decrease by one
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=10)

        HistoryEntry.objects.create(song=song)
        userp = UserProfile.objects.get(user=self.user)
        before = song.global_score

        # do a first call
        call_command('ircdislike', userp.ircnick)

        # second call
        call_command('ircdislike', userp.ircnick)

        self.assertEqual(before, 10)
        self.assertEqual(Song.objects.get(pk=song.id).global_score, 9)

    def test_ircdislike_nickdne(self):
        """
        Management command ircdislike

        The ircnick does not exist
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()
        nick = 'this_not_a_realnick'

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=9)

        HistoryEntry.objects.create(song=song)

        content = StringIO()
        call_command('ircdislike', nick, stderr=content)
        content.seek(0)
        output = content.read()

        self.assertEqual(Song.objects.get(pk=song.id).global_score, 9)
        self.assertEqual(output,
                         'nick [%s] does not exist' % nick)

    def test_ircdislike_nonick(self):
        """
        Management command ircdislike

        The nick is missing, no action
        """
        Song.objects.all().delete()
        HistoryEntry.objects.all().delete()

        song = Song.objects.create(artist='Lou Reed',
                                   album='Transformer',
                                   title='''song title''',
                                   genre='',
                                   score=0,
                                   family=0,
                                   global_score=0)

        HistoryEntry.objects.create(song=song)

        content = StringIO()
        call_command('ircdislike', stderr=content)
        content.seek(0)
        output = content.read()

        self.assertEqual(Song.objects.get(pk=song.id).global_score, 0)
        self.assertEqual(output,
                         "Erreur, vous devez indiquez un nick irc en option")
