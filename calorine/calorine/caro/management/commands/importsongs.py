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
Lookup for a song and to playlist
"""
from django.core.management.base import BaseCommand
from calorine.caro.models import Song
from calorine.caro.utils import importdir, checkid3, sigfile
from os.path import abspath, isdir
from calorine.utils.lastfm import get_tags
from calorine.caro.utils import importsong


class Command(BaseCommand):
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):

        exists = 0
        errors = 0
        update = 0
        insert = 0

        if len(args) > 0:
            dirpath = abspath(args[0])
        else:
            return "missing path, please add path to lookup\n"

        if not isdir(dirpath):
            return "path %s does not exists\n" % dirpath

        for fpath in importdir(dirpath):
            result = importsong(fpath)
            if result.startswith('[I]'):
                insert += 1
            elif result.startswith('[U]'):
                update += 1
            elif result.startswith('[X]'):
                exists += 1
            else:
                errors += 1

            self.stdout.write(result)

        self.stdout.write("%d songs already present db\n" % exists)
        self.stdout.write("%d songs path updated in db\n" % update)
        self.stdout.write("%d songs inserted in db\n" % insert)
        self.stdout.write("%d songs in error\n" % errors)

    def _donothing(self, song):
        """Do nothing but report
        """
        if song.genre == "":
            try:
                song.genre = ','.join(get_tags(song.artist, song.title))
                song.save()
            except TypeError:
                pass

        self.stdout.write("[.] %s - %s - %s\n" % (song.artist,
                                                  song.album,
                                                  song.title))

