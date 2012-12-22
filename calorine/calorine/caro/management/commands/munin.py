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
Some munin stats
"""

from django.core.management.base import BaseCommand
from calorine.caro.models import Song


class Command(BaseCommand):
    help = 'Print on stdout datas for munin'

    def handle(self, *args, **options):
        notfound = Song.objects.filter(score=-1000).count()
        neverplayed = Song.objects.filter(played=0).count()
        playedone = Song.objects.filter(played=1).count()
        playedmore = Song.objects.filter(played__gt=1).count()
        total = playedone + playedmore + neverplayed
        self.stdout.write("notfound.value %s\n" % notfound)
        self.stdout.write("neverplayed.value %s\n" % neverplayed)
        self.stdout.write("playedone.value %s\n" % playedone)
        self.stdout.write("playedmore.value %s\n" % playedmore)
        self.stdout.write("total.value %s\n" % total)
