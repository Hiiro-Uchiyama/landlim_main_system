from __future__ import unicode_literals
from django.contrib import admin
from .models import Category, Post, Tag, EasyApply
from django_summernote.admin import SummernoteModelAdmin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.conf import settings

admin.site.register(Tag)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, PostAdmin)

admin.site.register(Category)

admin.site.register(EasyApply)