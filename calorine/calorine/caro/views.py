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
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from django.shortcuts import render
from calorine.caro.models import Song
from calorine.caro.models import Logs
from calorine.caro.models import PlaylistEntry
from datetime import datetime
from django.views.generic import ListView


class SongList(ListView):
    queryset = Song.objects.filter(score__gt=0)
    paginate_by = 10
    template_name = "songs.html"
    context_object_name = "songs"


class PlayList(ListView):
    queryset = PlaylistEntry.objects.all()
    paginate_by = 10
    template_name = 'playlist.html'
    context_object_name = "songs"


class Profile(ListView):
    queryset = PlaylistEntry.objects.all().order_by('-pk')[:4]
    template_name = 'profile.html'
    context_object_name = "songs"


class LogList(ListView):
    queryset = Logs.objects.all().order_by('-date_import')
    template_name = 'errors.html'
    context_object_name = 'errors'


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
