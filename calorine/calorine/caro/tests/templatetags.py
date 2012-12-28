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
from django.test import TestCase, Client
from calorine.caro.models import Song
from calorine.caro.templatetags.lastfm import picture


class TemplateTagsTests(TestCase):  # pylint: disable-msg=R0904
    """
    TemplateTags

    """
    def get_picture(song, artist):
        """Redefine get_picture to simulate failed query
        """
        return None

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
