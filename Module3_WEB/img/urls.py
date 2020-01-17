from django.conf.urls import include, url
from . import views

app_name = 'img'

urlpatterns = [
    # /img/
    url(r'^$', views.index, name='index'),
    # /img/<album_id>/
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    # /img/<album_id>/favourite/
    url(r'^(?P<album_id>[0-9]+)/favourite/$', views.favourite, name='favourite'),
]
