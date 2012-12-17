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


class Command(BaseCommand):
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):

        exists = 0
        update = 0
        insert = 0

        if len(args) > 0:
            dirpath = abspath(args[0])
        else:
            return "missing path, please add path to lookup\n"

        if not isdir(dirpath):
            return "path %s does not exists\n" % dirpath

        for fpath in importdir(dirpath):
            tags = checkid3(fpath)
            if tags is not None:
                sig = sigfile(fpath)
                exsong = Song.objects.filter(uniq=sig)

                if len(exsong) > 0:
                    if exsong[0].filename != fpath:
                        self._updatesong(exsong[0], fpath)
                        update += 1
                    else:
                        self._donothing(exsong[0])
                        exists += 1
                else:
                    self._createsong(tags, sig, fpath)
                    insert += 1

        self.stdout.write("%d songs already present db\n" % exists)
        self.stdout.write("%d songs path updated in db\n" % update)
        self.stdout.write("%d songs inserted in db\n" % insert)

    def _donothing(self, song):
        """Do nothing but report
        """
        self.stdout.write("[.] %s - %s - %s\n" % (song.artist,
                                                  song.album,
                                                  song.title))

    def _updatesong(self, song, fpath):
        """Update the path if file moved
        """
        song.filename = fpath
        song.save()
        self.stdout.write("[U] %s\n" % song.title)

    def _createsong(self, tags, sig, fpath):
        """Create a new song in db
        """

        song = Song.objects.create(artist=tags['artist'],
                                   album=tags['album'],
                                   title=tags['title'],
                                   genre=tags['genre'],
                                   score=0,
                                   uniq=sig,
                                   global_score=0,
                                   filename=fpath)
        song.save()
        self.stdout.write("[I] %s\n" % song.title)
