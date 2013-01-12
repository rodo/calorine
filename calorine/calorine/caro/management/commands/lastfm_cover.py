# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
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
Lookup for cover with lastfm API
"""
from django.core.management.base import BaseCommand
from calorine.caro.models import Song
from calorine.caro.utils import picture


class Command(BaseCommand):
    help = 'Query lastfm API and add cover on it if found'

    def handle(self, *args, **options):
        i = 0
        songs = Song.objects.filter(cover__isnull=True)
        for song in songs:
            picture.delay(song)
            i += 1
            self.stdout.write("%d %s\n" % (i, song.title))
