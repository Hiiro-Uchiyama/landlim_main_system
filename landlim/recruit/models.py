from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget
from enum import Enum
from django.conf import settings
from django.core.validators import RegexValidator

class AccessLevelChoice(Enum):
    public = "Public"
    private = "Private"

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(created_at__lte=timezone.now())

class Tag(models.Model):
    tag = models.CharField('Tag', max_length=50)

    def __str__(self):
        return self.tag

class Category(models.Model):
    category = models.CharField('Category', max_length=50)

    def __str__(self):
        return self.category

class Post(models.Model):
    ## Register users who are looking for jobs.
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Recruiter')
    title = models.CharField('Title', max_length=50)
    text = models.TextField('Text')
    image = models.ImageField('Image', upload_to='recruit_images', blank=True, null=True)
    created_at = models.DateTimeField('Date', default=timezone.now)
    tag = models.ForeignKey(Tag, verbose_name = 'Tag', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, verbose_name = 'Category', on_delete=models.PROTECT)
    access_level = models.CharField('Public/Private', max_length=10, choices=[(level.name, level.value) for level in AccessLevelChoice], default='public')
    month = models.CharField('Month', max_length=10)
    date = models.CharField('Date', max_length=5)
    objects = PostQuerySet.as_manager()
    pin_x = models.FloatField('Pin_x')
    pin_y = models.FloatField('Pin_y')
    ## input in hiragana
    country = models.CharField(default='', max_length=20)
    prefecture = models.CharField(default='', max_length=20)
    city = models.CharField(default='', max_length=20)
    ## emotion
    emotion = models.CharField('Emotion', max_length=50)

    def __str__(self):
        return self.title

class EasyApply(models.Model):
    subject = models.CharField('Subject', max_length=50)
    text = models.TextField('Text')
    recruit = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='Recruit')
    username = models.CharField('Name', max_length=50)
    email = models.EmailField('Email')
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True)
    created_at = models.DateTimeField('Date', default=timezone.now)

    def __str__(self):
        return self.text