from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from calorine.caro.views import LogList, HistoryList
from calorine.caro.views import SongList, PlayList, Profile
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^accounts/', include('registration.urls')),
                       url(r'^accounts/profile/$', Profile.as_view()),
                       url(r'^songs/$', login_required(SongList.as_view())),
                       url(r'^logs$', login_required(LogList.as_view())),
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
