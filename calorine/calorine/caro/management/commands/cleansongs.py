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
Remove songs from database marke as file does not exists on filesystem
"""

from django.core.management.base import BaseCommand
from calorine.caro.models import Song


class Command(BaseCommand):
    help = 'Remove from db unonw on disk song'

    def handle(self, *args, **options):
        count = Song.objects.filter(score=-1000).count()
        Song.objects.filter(score=-1000).delete()
        msg = 'Successfully remove %d songs from database\n' % count
        self.stdout.write(msg)
