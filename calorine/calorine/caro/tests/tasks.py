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
from calorine.caro.models import Upload
from calorine.caro.tasks import addgenre
from calorine.caro.tasks import import_upload


class TasksTests(TestCase):  # pylint: disable-msg=R0904
    """
    TemplateTags

    """
    def test_addgenre(self):
        """Add genre
        """
        song = Song.objects.create(artist='Van Morrison',
                                   album='The Healing Game',
                                   title='Sometimes We Cry',
                                   genre='',
                                   score=0,
                                   played=0,
                                   family=0,
                                   global_score=0,
                                   cover='htt://foo.bar/img.png')

        result = addgenre.delay(song)

        self.assertTrue(result.task_id > 0)

    def test_import_upload(self):
        """
        Test with a picture with cover
        """
        Upload.objects.all().delete()
        upl = Upload.objects.create(uuid='123456789',
                                    path='/tmp/123456789',
                                    filename='The Healing Game.ogg',
                                    content_type='application/ogg')

        result = import_upload.delay(upl.uuid)

        self.assertTrue(result.task_id > 0)
