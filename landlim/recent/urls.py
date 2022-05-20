from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

app_name = "recent"

urlpatterns = [
    path('timeline/',views.recent, name='recent'),
    path('map/', views.local_map, name='local_map'),
    path('video/', views.recent_video, name='recent_video'),
    path('i18n/', include('django.conf.urls.i18n')),
]