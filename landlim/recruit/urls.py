from django.urls import path, include
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'recruit'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.recruit, name="recruit"),
    path('details/<int:post_id>/', views.detail, name='detail'),
    path('archive/<int:year>/',
         views.PostYearArchiveIndex.as_view(), name='year'),
    path('archive/<int:year>/<int:month>/',
         views.PostMonthArchiveIndex.as_view(), name='month'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('', views.PostList.as_view(), name='post_list'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('easy_apply/<int:user_id>/', views.easy_apply, name='easy_apply'),
    path('tag_list', views.tag_list, name="tag_list"),
    path('tag_linked_post/<int:tag_id>',views.tag_linked_post, name="tag_linked_post"),
    path('category_list', views.category_list, name="category_list"),
    path('category_linked_post/<int:category_id>',views.category_linked_post, name="category_linked_post")
]
