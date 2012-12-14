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
Add a random song in playlist
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
from datetime import datetime
from random import sample
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import Song


class Command(BaseCommand):
    help = 'Add a random song to playlist'

    def handle(self, *args, **options):
        rand_id = -1

        count = Song.objects.filter(family=0).count()
        if count > 1:
            rand_id = sample(xrange(1, count), 1)[0]
        else:
            rand_id = 0


        if rand_id >= 0:
            song = Song.objects.filter(family=0)[rand_id]
            PlaylistEntry.objects.create(
                song=song,
                date_add=datetime.utcnow().replace(tzinfo=utc),
                score=0)

            self.stdout.write('Add %s %s %s to playlist\n' % (song.artist,
                                                              song.title,
                                                              song.album))
