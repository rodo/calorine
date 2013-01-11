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
Models definition for caro app
"""
import logging
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models


class Song(models.Model):
    """
    The song object

    family :

      - 0 normal song
      - 1 jingles
    """
    artist = models.CharField(max_length=300,
                              verbose_name='artiste name',
                              blank=True)
    title = models.CharField(max_length=300,
                             verbose_name='titre',
                             blank=True)
    genre = models.CharField(max_length=300,
                             verbose_name='the song genre',
                             blank=True)
    album = models.CharField(max_length=300,
                             verbose_name='the song album',
                             blank=True)
    filename = models.CharField(max_length=300,
                                verbose_name='the filname',
                                blank=True)
    score = models.IntegerField(verbose_name='the song score',
                                blank=True)
    global_score = models.IntegerField(verbose_name='the song globalscore',
                                       blank=True)
    family = models.IntegerField(verbose_name='the song globalscore',
                                 default=0,
                                 db_index=True)
    played = models.IntegerField(blank=True,
                                 default=0)
    uniq = models.CharField(max_length=40, blank=True)

    cover = models.URLField(blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return self.title

    def add_to_playlist(self):
        """
        Add the song to playlist
        """
        PlaylistEntry.objects.create(
            song=self,
            date_add=datetime.now(),
            score=1)

    def userlike(self, user, note=1):
        """
        A user like this song
        """
        logger = logging.getLogger(__name__)
        logger.debug('user %s like song id %s with note %s' % (user.username,
                                                               self.id,
                                                               note))

        yesterday = datetime.today() - timedelta(hours=24)

        votes = Vote.objects.filter(song=self,
                                    user=user,
                                    date_vote__gt=yesterday)
        if len(votes) > 0:
            return 1
        else:
            # flag in memcache for this song/user
            song_key = 'song_{}_user_{}'.format(self.id, user.id)
            cache.set(song_key, True)

            self.global_score = self.global_score + note
            self.save()
            # create a vote for this song
            Vote.objects.create(song=self, user=user, vote=note)
            return 0


class PlaylistEntry(models.Model):
    """
    An entry in a playlist
    """
    song = models.ForeignKey(Song)
    date_add = models.DateTimeField()
    score = models.IntegerField(verbose_name='score', blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return "{}".format(self.song.title)  # pylint: disable-msg=E1101


class HistoryEntry(models.Model):
    """
    En entry in history

    """
    song = models.ForeignKey(Song)
    date_played = models.DateTimeField(auto_now_add=True)


class Logs(models.Model):
    """
    Logs information about misc actions like imports
    """
    filename = models.CharField(max_length=280)
    message = models.CharField(max_length=280)
    date_import = models.DateTimeField(auto_now_add=True)


class ArtistVote(models.Model):
    """
    A vote for an artist

    Each vote create an entry in this table with the artists's name

    """
    artist = models.CharField(max_length=300,
                              verbose_name='artiste name')
    date_vote = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField()


class Vote(models.Model):
    """
    En entry in history

    """
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    date_vote = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField()

    def save(self, *args, **kwargs):
        """
        Save method

        Create an artist vote
        """
        artist = self.song.artist  # pylint: disable-msg=E1101
        if artist != '':
            ArtistVote.objects.create(artist=artist, vote=self.vote)
        super(Vote, self).save(*args, **kwargs)


class Stream(models.Model):
    """
    Streams
    """
    url = models.URLField()


class Upload(models.Model):
    """
    A file uploaded

    """
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=64)
    path = models.CharField(max_length=300)
    filename = models.CharField(max_length=300)
    content_type = models.CharField(max_length=30)
    date_upload = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32,
                              default='starting',
                              db_index=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return self.filename


class Mime(models.Model):
    """
    Mime type and associate function

    """
    name = models.CharField(max_length=64)
    function = models.CharField(max_length=300)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #other fields here
    ircnick = models.CharField(max_length=64,
                               unique=True)

    def __str__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance,
                                                             ircnick=instance.username)

models.signals.post_save.connect(create_user_profile, sender=User)
