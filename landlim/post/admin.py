from django.contrib import admin
from .models import Post, PostImage, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tag_list')
    list_display_links = ('id', 'title')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(PostImage)

admin.site.register(Comment)