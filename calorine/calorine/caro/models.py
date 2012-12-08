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

"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from datetime import datetime

class Song(models.Model):
    """
    The song object
    """
    artist = models.CharField(max_length=300, verbose_name='titre', blank=True)
    title = models.CharField(max_length=300, verbose_name='titre', blank=True)
    genre = models.CharField(max_length=300, verbose_name='titre', blank=True)
    album = models.CharField(max_length=300, verbose_name='titre', blank=True)
    filename = models.CharField(max_length=300, verbose_name='titre', blank=True)
    score = models.IntegerField(verbose_name='titre', blank=True)
    played = models.IntegerField(blank=True, default=0)
    uniq = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return self.title

class PlaylistEntry(models.Model):
    """
    An entry in a playlist
    """
    song = models.ForeignKey(Song)
    date_add = models.DateTimeField()
    score = models.IntegerField(verbose_name='titre', blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return self.title


class HistoryEntry(models.Model):
    """
    En entry in history

    """
    song = models.ForeignKey(Song)
    date_played = models.DateTimeField()


class Logs(models.Model):
    """

    """
    filename = models.CharField(max_length=280)
    message = models.CharField(max_length=280)
    date_import = models.DateTimeField(auto_now_add=True)

