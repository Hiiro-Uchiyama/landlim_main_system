from django.conf.urls import url
from . import views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

app_name = "description"

urlpatterns = [
    path('about_landlim/', views.about_landlim, name="about_landlim"),
    path('about_landlim_web_edition/', views.about_landlim_web_edition, name="about_landlim_web_edition"),
    path('about_landlim_mobile_edition/', views.about_landlim_mobile_edition, name="about_landlim_mobile_edition"),
    path('about_landlim_api_system/', views.about_landlim_api_system, name="about_landlim_api_system"),
    path('about_landlim_network_system/', views.about_landlim_network_system, name="about_landlim_network_system"),
    path('about_landlim_recruitment_system/', views.about_landlim_recruitment_system, name="about_landlim_recruitment_system"),
    path('i18n/', include('django.conf.urls.i18n')),
]