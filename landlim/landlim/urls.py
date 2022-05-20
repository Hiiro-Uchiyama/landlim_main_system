from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from message.urls import router as message_router
from blog.api.routers import router as blog_router
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    ## API to perform login
    path('mobile_login/', obtain_jwt_token),
    path('mobile_accounts_api/', include('accounts.api.routers')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('post/', include('post.urls')),
    path('guide/', include('guide.urls')),
    path('want_todo/', include('want_todo.urls')),
    path('contact/', include('contact.urls')),
    path('notification/', include('notification.urls')),
    path('search_post/', include('search_post.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('account/', include('allauth.urls')),
    path('report/', include('report.urls')),
    path('recent/', include('recent.urls')),
    path('recruit/', include('recruit.urls')),
    path('blog/', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('api/blog/', include(blog_router.urls)),
)
