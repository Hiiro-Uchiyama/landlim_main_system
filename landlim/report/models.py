from __future__ import unicode_literals
from django.db import models
from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from post.models import Post

class Report(models.Model):
    title = models.CharField('ReportTitle', max_length=55)
    text = models.CharField('ReportText', max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ReportUser')
    report = models.ManyToManyField(Post, verbose_name='Report', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username