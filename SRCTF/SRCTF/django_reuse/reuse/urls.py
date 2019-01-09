from django.conf.urls import url, include
from . import views
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<catid>[0-9]+)/$', views.cat_view, name='catview'),
    url(r'^(?P<catid>[0-9]+)/(?P<ctfid>[0-9]+)$', views.ctf_view, name='ctfview'),
    url(r'^yourctf/$', views.your_ctf, name='yourctf'),
    url(r'^about/$', views.about, name='about'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page':'/'}),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),

]
