from django.conf.urls import patterns, url
from video import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^watch/(?P<video_id>[\w\-]+)/$', views.watchVid, name='watchVid'),
    url(r'^search/$', views.search, name='search'),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^random/$', views.random, name='random'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^search/(?P<tag>[\w\-]+)/$', views.search, name='tagsearch'),
    url(r'^requesto/$', views.requesto, name="requesto"),
    url(r'^info/$', views.info, name="info"),
    )