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
irclike
"""
import logging
from django.core.management.base import BaseCommand
from calorine.caro.models import UserProfile
from calorine.caro.models import HistoryEntry
from calorine.caro.models import Song

class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):

        if len(args) == 0:
            print "Erreur, vous devez indiquez un nick irc en option"
            return -1

        result = self.irclike(args[0])

        if result == -1:
            raise CommandError('Poll "%s" does not exist' % args[0])
        

    def irclike(self, nick):
        """
        An irc user like the actual song
        """
        logger = logging.getLogger(__name__)
        try:
            userp = UserProfile.objects.get(ircnick=nick)
        except UserProfile.DoesNotExist:
            logger.warning("ircnick [%s] does not exists" % (nick))
            return -1
        
        songs = HistoryEntry.objects.values('song').order_by('-pk')[:1]
        song = Song.objects.get(pk=songs[0]['song'])
        song.userlike(userp.user)

