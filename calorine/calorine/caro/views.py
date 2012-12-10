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
The django views
"""
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from calorine.caro.models import Song
from calorine.caro.models import Logs
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import HistoryEntry
from datetime import datetime
from django.views.generic import ListView
from django.core.cache import cache


class SongList(ListView):
    queryset = Song.objects.filter(score__gte=0)
    paginate_by = 10
    template_name = "songs.html"
    context_object_name = "songs"


class HistoryList(ListView):
    queryset = HistoryEntry.objects.all().order_by("-date_played")
    paginate_by = 10
    template_name = 'history.html'
    context_object_name = "songs"


class PlayList(ListView):
    queryset = PlaylistEntry.objects.all().order_by("-score")
    paginate_by = 10
    template_name = 'playlist.html'
    context_object_name = "songs"

    def get_context_data(self, **kwargs):
        context = super(PlayList, self).get_context_data(**kwargs)
        for ple in context['songs']:
            if cache.get('ple_{}_{}'.format(self.request.user.id,
                                            ple.song.pk,
                                            ple.pk)):
                ple.vote = True
        return context


class Profile(ListView):
    queryset = PlaylistEntry.objects.all().order_by('-pk')[:4]
    template_name = 'profile.html'
    context_object_name = "songs"


class LogList(ListView):
    queryset = Logs.objects.all().order_by('-date_import')
    template_name = 'errors.html'
    context_object_name = 'errors'
    paginate_by = 10


def pladd(request, song_id):
    """
    The songs in databases
    """
    song = get_object_or_404(Song, pk=song_id)

    ple = PlaylistEntry(song=song,
                        score=1,
                        date_add=datetime.today())
    ple.save()

    return render(request, 'playlist_add.html')


def pldislike(request, pk):
    """
    dislike a song in Playlist
    """
    return inc_desc("less", request, pk)


def pllike(request, pk):
    """
    Like a song
    """
    return inc_desc("plus", request, pk)


def inc_desc(sign, request, pk):
    """
    Need doc
    """
    ple = get_object_or_404(PlaylistEntry, pk=pk)
    key = 'ple_{}_{}'.format(request.user.id, ple.song.pk, ple.pk)
    if cache.get(key):
        return HttpResponse(
            json.dumps({'message': 'Do not try this with me'}),
            mimetype="application/json")
    else:
        cache.set(key, True)
    if sign == "plus":
        ple.score += 1
    else:
        ple.score -= 1
    ple.save()
    resp = {'score': ple.score, 'id': ple.pk}
    return HttpResponse(
        json.dumps({'entry': resp}),
        mimetype="application/json")
