from django.conf.urls import url
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

app_name = "contact"

urlpatterns = [
    url(r'^$', views.post_contact, name='post_contact'),
    path('i18n/', include('django.conf.urls.i18n')),
]