from django.conf.urls import url
from . import views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('notion', views.notion_list, name="notion_list"),
]