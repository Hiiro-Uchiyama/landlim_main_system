from collections import namedtuple
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views

app_name = "post"

urlpatterns = [
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^save_your_location/$', views.save_your_location, name='save_your_location'),
    url(r'^update_post/(?P<post_pk>\d+)/$', views.update_post, name='update_post'),
    url(r'^this_post/(?P<pk>\d+)/$', views.this_post, name='this_post'),
    url(r'^delete_post/(?P<post_pk>\d+)/$', views.post_delete, name='delete_post'),
    url(r'^post_details/(?P<pk>\d+)/$', views.post_details, name='post_details'),
    path('post_details/<int:pk>/', views.PostDetail.as_view(), name='post_details'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('comment_like/', views.comment_like, name='comment_like'),
    path('discomment_like/', views.discomment_like, name='discomment_like'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('liked_timeline/', views.liked_timeline, name='liked_timeline'),
    path('tag_linked_post/<int:tag_id>', views.tag_linked_post, name="tag_linked_post"),
    path('country_linked_post/<str:country>',views.country_linked_post, name="country_linked_post"),
    path('prefecture_linked_post/<str:prefecture>', views.prefecture_linked_post, name="prefecture_linked_post"),
    path('city_linked_post/<str:city>',views.city_linked_post, name="city_linked_post"),
    path('emotion_linked_post/<str:emotion>',views.emotion_linked_post, name="emotion_linked_post"),
    path('emotion_visualization', views.emotion_visualization, name="emotion_visualization"),
    path('liked_user_list/<int:pk>', views.liked_user_list, name="liked_user_list"),
]
