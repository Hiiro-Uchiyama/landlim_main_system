from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
import bookmark

app_name = "bookmark"

## The name of the link should identify the location of the bookmark.
urlpatterns = [
    path('', views.bookmark, name='bookmark'),
    path('map', views.bookmark_map, name='bookmark_map'),
    path('bookmark_ajax/', views.bookmark_ajax, name='bookmark_ajax'),
    path('i18n/', include('django.conf.urls.i18n')),
]
