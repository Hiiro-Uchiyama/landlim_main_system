from __future__ import unicode_literals
from django.db import models
from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from post.models import Post

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='BookmarkUser')
    post = models.ManyToManyField(Post, verbose_name='BookmarkPost', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def bookmark_count(self):
        return self.post.count()

    def __str__(self):
        return self.user.username