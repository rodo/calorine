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
Add a random song to the playlist
"""
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from datetime import datetime
from random import sample
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import Song


class Command(BaseCommand):
    help = 'Add a random song to the playlist'

    def handle(self, *args, **options):
        """Handle the command
        """
        count = Song.objects.filter(family=0).count()

        if count > 0:
            song = self.getrandomsong(count)
            self.addsong(song)

    def getrandomsong(self, count):
        """
        Get a random song
        """
        if count > 1:
            rand_id = sample(xrange(1, count), 1)[0]
        else:
            rand_id = 0

        return Song.objects.filter(family=0)[rand_id]

    def addsong(self, song):
        """
        Add a song to the playlist
        """

        PlaylistEntry.objects.create(
            song=song,
            date_add=datetime.utcnow().replace(tzinfo=utc),
            score=1)

        self.stdout.write('Add %s %s %s to playlist\n' % (song.artist,
                                                          song.title,
                                                          song.album))
