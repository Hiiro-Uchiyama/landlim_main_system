from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

app_name = "accounts"

urlpatterns = [
    url(r'^signup/$',views.signup_accounts, name='signup_accounts'),
    url(r'^login/$',views.login_accounts, name='login_accounts'),
    url(r'^logout/$', views.logout_accounts, name='logout_accounts'),
    url(r'^own_page/$', views.own_page, name='own_page'),
    url(r'^edit/$', views.edit_accounts, name='edit_accounts'),
    url(r'^others_page/(?P<user_pk>\d+)/$', views.others_page, name='others_page'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activation, name='activation'),
    url(r'^password/reset/$', views.password_reset, name='reset-password'),
    url(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='reset-password-done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='reset-password-confirm'),
    url(r'password/reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_from_key_done.html'), name='reset-password-complete'),
    url(r'^delete/$', views.delete_accounts, name='delete_accounts'),
    url(r'^like_list/$', views.like_list, name='like_list'),
    url(r'^like_map/$', views.like_map, name='like_map'),
    path('follow_unfollow/', views.follow_unfollow, name='follow_unfollow'),
    path('block_unblock/', views.block_unblock, name='block_unblock'),
    path('following/', views.following_list, name='following_list'),
    path('follower/', views.follower_list, name='follower_list'),
    path('friends_map/', views.friends_map, name='friends_map'),
    path('friends_timeline/', views.friends_timeline, name='friends_timeline'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('get_your_position/', views.get_your_position, name="get_your_position"),
]
