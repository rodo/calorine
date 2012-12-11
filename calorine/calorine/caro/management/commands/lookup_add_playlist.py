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
Lookup for a song and to playlist
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
from haystack.query import SearchQuerySet
from datetime import datetime
from random import sample
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import Song
import os

class Command(BaseCommand):
    help = 'Lookup for a song and add it to playlist'

    def handle(self, *args, **options):
        
        if len(args) > 0:
            qry_str = args[0]

            try:
                srchqry = SearchQuerySet().filter(content__contains=qry_str).models(Song)
                results = [ r.pk for r in srchqry ]

                count = Song.objects.filter(pk__in=results).count()
                if count > 0:
                    rand_id = sample(xrange(1, count), 1)[0]
                    song = Song.objects.filter(pk__in=results)[rand_id]
                    ple = PlaylistEntry.objects.create(
                        song=song,
                        date_add=datetime.utcnow().replace(tzinfo=utc),
                        score=0)
                    self.stdout.write('%s - %s - %s est dans playlist\n' % (song.artist,
                                                                            song.title,
                                                                            song.album))
                else:
                    self.stdout.write('On a rien trouvé')
            except Song.DoesNotExist:
                raise CommandError('Unable to find a song')


