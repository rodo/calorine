# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
Shuffle the songs in playlist
"""
from django.core.management.base import BaseCommand
from random import shuffle
from calorine.caro.models import PlaylistEntry


class Command(BaseCommand):
    help = 'Shuffle the playlist'

    def handle(self, *args, **options):
        """Handle the command
        """
        plls = PlaylistEntry.objects.all()
        datas = self.getrandoms(len(plls))
        for ple in plls:
            ple.rank = datas.pop()
            ple.save()

    def getrandoms(self, count):
        """Get a random array
        """
        datas = range(1, count + 1)
        shuffle(datas)
        return datas
