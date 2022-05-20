from accounts.views import delete_accounts
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = "want_todo"

urlpatterns = [
    path('', views.want_todo_list, name='want_todo_list'),
    path('map/', views.want_todo_map, name='want_todo_map'),
    path('add_want_todo/', views.add_want_todo, name='add_want_todo'),
    path('delete_want_todo/<int:pk>/', views.delete_want_todo, name='delete_want_todo'),
    path('i18n/', include('django.conf.urls.i18n')),
]