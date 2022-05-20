from email.policy import default
import os
from django import forms
from django.contrib import messages
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict
from blog.models import Tag as BlogTag
## Module required for 2-step verification of e-mail addresses
from .emails import send_accounts_activation_email
from django.utils.encoding import force_bytes, force_text
from django_file_validator.validators import MaxSizeValidator
from django.contrib.auth.tokens import default_token_generator
from versatileimagefield.placeholder import OnDiscPlaceholderImage
from django.contrib.auth.validators import UnicodeUsernameValidator
from versatileimagefield.fields import PPOIField, VersatileImageField
from django.utils.translation import LANGUAGE_SESSION_KEY, pgettext_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail, delete
import uuid
## Perform multilingualization within the model file.
from django.utils.translation import gettext_lazy as _

## Function to specify path to save icon
class Icon_directory_path(object):
    def icon_directory_path(instance, filename):
        return 'icon/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

## Function to generate a path for storing a background image.
class Background_directory_path(object):
    def background_directory_path(instance, filename):
        return 'background/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

## A model for managing users.
class UserManager(BaseUserManager):

    def create_user(
            self, username, email, password=None,
            **extra_fields):
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username, email=email,
            **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def _create_user(self, username, email, password, **extra_fields):
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username, email=email,
            **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        to_email_address = email
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        context = {'uid': uidb64, 'token': token}
        send_accounts_activation_email(context, to_email_address)
        return user

    def create_superuser(self, username, password, **extra_fields):
        email = 'log.hiiro@gmail.com'
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

## Wouldn't it be better to tie them together based on emotion?
class User(PermissionsMixin, AbstractBaseUser):
    ## Username and username validator
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('Username'),
        max_length=150,
        unique=True,
        help_text=(
            'You can use alphanumeric characters and @, . , +, -, and _ can be used. 英数字と@, ., +, -, _が使えます。'),
        validators=[username_validator],
        error_messages={
            'unique': ("This user name has already been registered. このユーザ名は既に登録されています。"),
        },
    )
    ## Ad user registration.
    ## Maybe it would be good to manage transfers, etc.
    commercial_user_or_not = models.BooleanField(default=False)
    ## Are you an official Landrim user?
    official_user_or_not = models.BooleanField(default=False)
    ## Basic Information
    email = models.EmailField('Email', unique=True)
    description = models.CharField('Description', max_length=200, blank=True)
    hobby = models.CharField('Hobby', max_length=100, blank=True)
    nickname = models.CharField('Nickname', max_length=50, blank=True)
    ## social link
    web_link = models.URLField('WebLink', blank=True)
    twitter_link = models.URLField('TwitterLink', blank=True)
    instagram_link = models.URLField('InstagramLink', blank=True)
    facebook_link = models.URLField('FacebookLink', blank=True)
    ## Date Data
    last_login = models.DateTimeField(default=timezone.now, editable=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    date_out = models.DateTimeField(default=timezone.now, editable=False)
    ## authority
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    ## Icons and Background Images
    icon = VersatileImageField('Icon', upload_to=Icon_directory_path.icon_directory_path, blank=True, validators=[MaxSizeValidator(2048)])
    background = VersatileImageField('Background', upload_to=Background_directory_path.background_directory_path, blank=True, validators=[MaxSizeValidator(2048)])
    ## Various settings
    want_messages = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    ## Countries and Regions
    country = models.CharField('Country', max_length=30, blank=True)
    prefecture = models.CharField('Prefecture', max_length=20, blank=True)
    city = models.CharField('City', max_length=30, blank=True)
    ## Relationships with people
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Following', default=None, blank=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Follower', default=None, blank=True)
    blocking = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Blocking', default=None, blank=True)
    ## Special settings
    emotion = models.CharField('UserEmotion', max_length=100, blank=True)
    ## It supports input by color code or RGB.
    color = models.CharField('UserColor', max_length=100, blank=True)
    ## Have them turn on and save the location information of the places where they are usually active.
    pin_x = models.FloatField(blank=True, null=True)
    pin_y = models.FloatField(blank=True, null=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    objects = UserManager()

    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.thumbnail['200x200'].url

    def get_following_num(self):
        return self.following.all().count()

    def get_follower_num(self):
        return self.follower.all().count()

    def get_blocking_num(self):
        return self.blocking.all().count()

    @receiver(user_signed_up)
    def user_signed_up_(request, user, **kwargs):
        user.is_active = True
        user.is_staff = False
        user.save()

    def __str__(self):
        return self.username
