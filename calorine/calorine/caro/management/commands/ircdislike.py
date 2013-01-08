#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
command used by the irc bot. When a user like a song the global_score
is increase by one
"""
import logging
from django.core.management.base import BaseCommand
from calorine.caro.models import UserProfile
from calorine.caro.models import HistoryEntry
from calorine.caro.models import Song

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ircnick>'
    help = 'dislike a song from an irc account'

    songtitle = ''

    def handle(self, *args, **options):

        if len(args) == 0:
            msg = "Erreur, vous devez indiquez un nick irc en option"
            logger.warning("ircnick is missing")
            self.stderr.write(msg)
            return "\n"

        result = self.ircdislike(args[0])

        if result == -1:
            logger.warning('nick [%s] does not exist' % args[0])
            self.stderr.write('nick [%s] does not exist' % args[0])
            return "\n"
        else:
            msg = '''Ok tu n'aimes pas %s, c'est noté''' % self.songtitle
            self.stdout.write(msg)
            return "\n"
            
    def ircdislike(self, nick):
        """
        An irc user dislike the current playing song
        """
        try:
            userp = UserProfile.objects.get(ircnick=nick)
        except UserProfile.DoesNotExist:
            logger.warning("ircnick [%s] does not exists" % (nick))
            return -1

        songs = HistoryEntry.objects.values('song').order_by('-pk')[:1]
        song = Song.objects.get(pk=songs[0]['song'])
        self.songtitle = song.title
        song.userlike(userp.user, -1)

        return 0
