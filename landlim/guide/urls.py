from django.conf.urls import url
from . import views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

app_name = "guide"

urlpatterns = [
    url(r'^landlim_guide$', views.landlim_guide, name='landlim_guide'),
    url(r'^landlim_faqs$', views.landlim_faqs, name='landlim_faqs'),
    url(r'^landlim_about$', views.landlim_about, name='landlim_about'),
    path('i18n/', include('django.conf.urls.i18n')),
]