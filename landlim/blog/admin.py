from __future__ import unicode_literals
from django.contrib import admin
from .models import Category, Comment, Post, Tag
from django_summernote.admin import SummernoteModelAdmin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.conf import settings

## Admin rights for tags and their display in the admin panel
admin.site.register(Tag)

## Summer Notes added and posts added.
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, PostAdmin)

admin.site.register(Category)

admin.site.register(Comment)
