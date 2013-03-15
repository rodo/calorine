# -*- coding: utf-8 -*-
#
# Copyright (c) 2012,2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
Unit tests for template tags in caro

"""
from django.test import TestCase
from calorine.caro.models import Song
from calorine.caro.templatetags.lastfm import picture


class TemplateTagsTests(TestCase):  # pylint: disable-msg=R0904
    """
    TemplateTags
    """

    def test_picture(self):
        """
        Test with a picture with cover
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='Blues',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0,
                                   cover='htt://foo.bar/img.png')

        response = picture(song)
        attend = {'picture': song.cover}
        self.assertEqual(response, attend)

    def test_picture_baddatas(self):
        """
        Test with a song that must nor return a cover
        """
        song = Song.objects.create(artist='Foobar',
                                   album='Sure this album does not exists',
                                   title='Lorem ipsum',
                                   genre='Ipsum',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0,
                                   cover='htt://foo.bar/img.png')

        response = picture(song)
        attend = {'picture': song.cover}
        self.assertEqual(response, attend)

    def test_picture_baddatas2(self):
        """
        Test with a song that must not return a cover
        """
        song = Song.objects.create(artist='Foobar',
                                   album='Sure this album does not exists',
                                   title='Lorem ipsum',
                                   genre='Ipsum',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0)

        response = picture(song)
        attend = {'picture': 'http://lorempixel.com/64/64/animals/'}
        self.assertEqual(response, attend)

    def test_picture2(self):
        """
        Test with a picture with cover
        """
        song = Song.objects.create(artist='U2',
                                   album='Rattle and Hum',
                                   title='Love rescue me',
                                   genre='Rock',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0)

        response = picture(song)
        url = u'http://userserve-ak.last.fm/serve/64s/57976973.png'
        attend = {'picture': url}
        self.assertEqual(response, attend)
