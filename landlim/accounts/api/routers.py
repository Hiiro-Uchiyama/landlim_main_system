from django.urls import path
from rest_framework import routers
from .view_set import AuthSignUp, AuthInfoGetView, AuthInfoUpdateView

## As for deletions and partial updates, why not just do it on the web?
urlpatterns = [
    path('mobile_signup/', AuthSignUp.as_view()),
    path('mobile_own_page/', AuthInfoGetView.as_view()),
    path('mobile_own_info_update/', AuthInfoUpdateView.as_view()),
]