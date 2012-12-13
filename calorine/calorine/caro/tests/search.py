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
from haystack.query import SearchQuerySet
from django.test.utils import override_settings


class SearchTests(TestCase):  # pylint: disable-msg=R0904
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


    @override_settings(HAYSTACK_CONNECTIONS = {
            'default': {
                'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
                'PATH': '/tmp/whoosh_index'}})
    def test_bycontent(self):
        """
        Use haystack search on content
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   family=0,
                                   global_score=0)

        srchqry = SearchQuerySet().all()
        results = [int(r.pk) for r in srchqry]
        self.assertTrue(len(srchqry) > 0)
        self.assertTrue(song.id in results)

    def test_bytitle(self):
        """
        Use haystack search on title
        """
        song = Song.objects.create(artist='Pixies',
                                   album='Death to the Pixies',
                                   title='Caribou',
                                   genre='Rock',
                                   score=0,
                                   family=0,
                                   global_score=0)

        nbr = len(SearchQuerySet().filter(
                title__contains='caribou').models(Song))

        self.assertEqual(nbr, 1)

    def test_byartist(self):
        """
        Use haystack search on artist
        """
    
        Song.objects.create(artist='Popa Chubby',
                            album='''How'd a White Boy Get the Blues?''',
                            title='No Comfort', 
                            genre='Rock',
                            score=0,
                            family=0,
                            global_score=0)

        nbr = len(SearchQuerySet().filter(
                artist__contains='popa').models(Song))

        self.assertEqual(nbr, 1)



