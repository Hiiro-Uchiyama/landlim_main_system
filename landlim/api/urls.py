from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

app_name = "api"

urlpatterns = []