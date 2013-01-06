from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from calorine.caro.views import LogList, HistoryList
from calorine.caro.views import SongList, PlayList
from calorine.caro.views import PopsList
from calorine.caro.views import StarList
from calorine.caro.views import NeverList
from calorine.caro.views import ArtistList
from calorine.caro.views import UglyList
from calorine.caro.views import UploadList
from calorine.caro.views import profile, cover
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',                       
                       url(r'^accounts/', include('registration.urls')),
                       url(r'^accounts/profile/$', 'calorine.caro.views.profile'),
                       url(r'^upload/$', 'calorine.caro.views.upload'),
                       url(r'^uploads/$', login_required(UploadList.as_view())),
                       url(r'^cover/(?P<cover>.*)$', 'calorine.caro.views.cover'),
                       url(r'^onair.json$', 'calorine.caro.views.onair'),
                       url(r'^songs/$', login_required(SongList.as_view())),
                       url(r'^stars/$', login_required(StarList.as_view())),
                       url(r'^stats/artist/$', login_required(ArtistList.as_view())),
                       url(r'^stats/ugly/$', login_required(UglyList.as_view())),
                       url(r'^songs/pops/$', login_required(PopsList.as_view())),
                       url(r'^songs/never-played/$', login_required(NeverList.as_view())),
                       url(r'^logs/$', login_required(LogList.as_view())),
                       url(r'^history/', login_required(HistoryList.as_view())),
                       url(r'^playlist/add/(?P<song_id>\d+)$', 'calorine.caro.views.pladd'),
                       url(r'^playlist/inc/(?P<pk>\d+)$', 'calorine.caro.views.pllike'),
                       url(r'^playlist/dec/(?P<pk>\d+)$', 'calorine.caro.views.pldislike'),
                       url(r'^$', login_required(PlayList.as_view()), name="playlist"),
                       url(r'^admin/', include(admin.site.urls)),
                       )
# Examples:
# url(r'^$', 'calorine.views.home', name='home'),
# url(r'^calorine/', include('calorine.foo.urls')),
# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
# Uncomment the next line to enable the admin:
