from django.conf.urls import url
from . import views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

app_name = "search_post"

urlpatterns = [
    path('api/posts/get/', views.api_posts_get, name='api_posts_get'),
    path('api/tags/get/', views.api_tags_get, name='api_tags_get'),
    path('api/cou/get/', views.api_cou_get, name='api_cou_get'),
    path('api/pre/get/', views.api_pre_get, name='api_pre_get'),
    path('api/cit/get/', views.api_cit_get, name='api_cit_get'),
    path('api/emo/get/', views.api_emo_get, name='api_emo_get'),
    url(r'^post/$', views.search_post, name='search_post'),
    url(r'^post/by/tag/$', views.search_tag, name='search_by_tag'),
    url(r'^post/by/area_cou/$', views.search_area_cou, name='search_by_area_cou'),
    url(r'^post/by/area_city/$', views.search_area_city, name='search_by_area_city'),
    url(r'^post/by/emotion/$', views.search_emotion, name='search_by_emotion'),
    url(r'^post/ajax/$', views.search_post_ajax, name='search_post_ajax'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('post/refine/', views.search_refine, name='search_refine'),
]
