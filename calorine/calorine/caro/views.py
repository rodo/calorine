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
import logging
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Q
from datetime import datetime
from django.views.generic import ListView
from django.core.cache import cache
from haystack.query import SearchQuerySet
from uuid import uuid4
from calorine.caro.models import Song
from calorine.caro.models import Logs
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import HistoryEntry
from calorine.caro.models import Vote
from calorine.caro.models import Upload
from calorine.caro.models import ArtistVote
from calorine.caro.models import Stream
from calorine.caro.utils import onair_datas
from calorine.caro.utils import clean_cache
from calorine.caro.tasks import import_upload
from django.contrib.auth.decorators import login_required


def build_search_query(query):
    """Buil the search query
    """
    if query.startswith('artist:'):
        sqs = SearchQuerySet().filter(artist__contains=query[7:]).models(Song)
    else:
        sqs = SearchQuerySet().filter(content__contains=query).models(Song)
    return sqs


class SongList(ListView):
    paginate_by = 17
    template_name = "songs.html"
    context_object_name = "songs"

    def get_queryset(self):
        """
        Use the same class for search en listview
        """
        qry_str = self.request.GET.get('q')

        if qry_str is not None:
            srchqry = build_search_query(qry_str)
            results = [r.pk for r in srchqry]
            queryset = Song.objects.filter(pk__in=results)
        else:
            queryset = Song.objects.filter(score__gte=0, family=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SongList, self).get_context_data(**kwargs)
        for song in context['songs']:
            if cache.get('song_{}'.format(song.pk)):
                song.vote = True
        return context


class HistoryList(ListView):
    queryset = HistoryEntry.objects.all().order_by("-date_played")
    paginate_by = 17
    template_name = 'history.html'
    context_object_name = "songs"


class PopsList(ListView):
    queryset = Song.objects.all().order_by("-global_score")
    paginate_by = 17
    template_name = 'songs.html'
    context_object_name = "songs"


class NeverList(ListView):
    queryset = Song.objects.filter(played=0)
    paginate_by = 17
    template_name = 'songs.html'
    context_object_name = "songs"

    def get_context_data(self, **kwargs):
        context = super(NeverList, self).get_context_data(**kwargs)
        for song in context['songs']:
            if cache.get('song_{}'.format(song.pk)):
                song.vote = True
        return context


class ArtistList(ListView):
    queryset = ArtistVote.objects.values(
        'artist').filter(vote=1).annotate(
        artist_count=Count('artist')).order_by('-artist_count')
    paginate_by = 17
    template_name = 'stats.html'
    context_object_name = "songs"


class StarList(ListView):
    queryset = Vote.objects.values('user').annotate(
        dcount=Count('user')).order_by('-dcount')
    paginate_by = 17
    template_name = 'stars.html'
    context_object_name = "stars"

    def get_context_data(self, **kwargs):
        context = super(StarList, self).get_context_data(**kwargs)
        total = 0.0
        for star in context['stars']:
            total = total + float(star['dcount'])
        for star in context['stars']:
            star['ouser'] = get_object_or_404(User, pk=star['user'])
            star['percent'] = int(100.0 * float(star['dcount']) / total)
        return context


class PlayList(ListView):
    queryset = PlaylistEntry.objects.all().order_by('-score', 'date_add')
    paginate_by = 17
    template_name = 'playlist.html'
    context_object_name = "songs"

    def get_context_data(self, **kwargs):
        context = super(PlayList, self).get_context_data(**kwargs)
        for ple in context['songs']:
            if cache.get('ple_{}_{}'.format(self.request.user.id,
                                            ple.pk)):
                ple.vote = True
        return context


class LogList(ListView):
    queryset = Logs.objects.all().order_by('-date_import')
    template_name = 'errors.html'
    context_object_name = 'errors'
    paginate_by = 17


class UglyList(ListView):
    queryset = Song.objects.filter(Q(title='') | Q(artist='') | Q(album='') | Q(genre='')).order_by('artist')
    template_name = 'ugly.html'
    context_object_name = 'songs'
    paginate_by = 17



class UploadList(ListView):
    """Upload songs
    """
    queryset = Upload.objects.all().order_by("-pk")
    paginate_by = 17
    template_name = 'uploads.html'
    context_object_name = "uploads"


@login_required
def profile(request):
    """The profile wiew
    """
    ples = PlaylistEntry.objects.all().order_by('-score', 'date_add')[:4]
    songs = Song.objects.all().order_by('-pk')[:4]
    uploads = Upload.objects.all().order_by('-pk')[:4]
    streams = Stream.objects.all()
    template_name = 'profile.html'

    return render(request,
                  template_name,
                  {'songs': songs,
                   'uploads': uploads,
                   'ples': ples,
                   'streams': streams,
                   'uuid': str(uuid4()),
                   })


@login_required
def upload(request):
    """Upload songs
    """
    uploads = Upload.objects.all().order_by('-pk')[:42]
    filename = '%s' % (request.POST['songname.name'])
    uuid = request.GET['X-Progress-ID']
    upl = Upload.objects.create(uuid=uuid,
                                path=request.POST['songname.path'],
                                filename=filename,
                                content_type=request.POST['songname.content_type'])

    logger = logging.getLogger(__name__)
    logger.info("upload [%s] %s" % (filename, uuid))
    # launch a celery task
    import_upload.delay(uuid)

    return render(request,
                  'upload.html',
                  {'uploads': uploads,
                   'path': request.POST['songname.path'],
                   'filename': request.POST['songname.name'],
                   'type': request.POST['songname.content_type'],
                   'uuid': str(uuid4())
                   })


@login_required
def cover(request, cover):
    """The profile wiew
    """
    data = cache.get("%s_data" % cover)
    mode = cache.get("%s_mode" % cover)
    size = cache.get("%s_size" % cover)

    #img = Image.new(mode, size)
    img = Image.fromstring(mode, size, data)

    response = HttpResponse(mimetype='image/jpeg')
    response.write(img)

    return response


@login_required
def onair(request):
    """The onair view
    """
    datas = onair_datas()

    response = HttpResponse(mimetype='application/json; charset=utf-8')

    from json import dumps
    response.write(dumps(datas))

    return response


@login_required
def pladd(request, song_id):
    """
    The songs in databases
    """
    song = get_object_or_404(Song, pk=song_id)

    ple = PlaylistEntry.objects.create(song=song,
                                       score=0,
                                       date_add=datetime.today())

    clean_cache(request.user.id, song.id, ple.id)
    pllike(request, ple.pk)
    return render(request, 'playlist_add.html')


def pldislike(request, pk):
    """
    dislike a song in Playlist
    """
    return inc_desc("less", request, pk)


@login_required
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
    key = 'ple_{}_{}'.format(request.user.id, ple.pk)
    song_key = 'song_{}'.format(ple.song.pk)

    if cache.get(key):
        return HttpResponse(
            json.dumps({'message': 'Do not try this with me'}),
            mimetype="application/json")
    else:
        cache.set(key, True)
        cache.set(song_key, True)

    song = get_object_or_404(Song, pk=ple.song.id)

    if sign == "plus":
        ple.score += 1
        song.global_score += 1
        vte = +1
    else:
        ple.score -= 1
        song.global_score -= 1
        vte = -1
    ple.save()
    song.save()
    # create a vote for this song
    Vote.objects.create(song=song, user=request.user, vote=vte)

    resp = {'score': ple.score, 'id': ple.pk}
    return HttpResponse(
        json.dumps({'entry': resp}),
        mimetype="application/json")
