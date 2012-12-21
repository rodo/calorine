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
Check if filename exists on disk
"""
from django.core.management.base import BaseCommand
from calorine.caro.models import Song
from os.path import isfile


class Command(BaseCommand):
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        missing = 0
        for song in Song.objects.all().order_by('filename'):
            if not isfile(song.filename):
                song.score = -1000
                song.save()
                missing += 1
                self.stdout.write("%s is missing\n" % song.filename)

        self.stdout.write("%d songs are missing\n" % missing)
