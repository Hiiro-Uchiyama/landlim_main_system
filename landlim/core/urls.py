from django.conf.urls import url
from . import views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    url(r'^$', views.first, name='first'),
    url(r'index/$', views.index, name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
]