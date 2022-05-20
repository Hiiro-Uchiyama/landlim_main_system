from email.policy import default
from re import T
from django.db import models
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.conf import settings
from django.db.models import F, Max, Q
from versatileimagefield.fields import PPOIField, VersatileImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
from versatileimagefield.placeholder import OnDiscPlaceholderImage
from django.core.exceptions import ValidationError
from enum import Enum
from django_file_validator.validators import MaxSizeValidator
from accounts.models import User
from taggit.managers import TaggableManager
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import uuid
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail, delete
from django.utils.deconstruct import deconstructible

## Should do a serious error catch.

class AccessLevelChoice(Enum):
    public = "Public"
    private = "Private"

def has_no_singlequote(value):
    if "\'" in value:
        raise ValidationError(
            'Do not include single quotes (\')',
            params={'value': value},
        )

@deconstructible
class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(created_at__lte=timezone.now())

class Video_directory_path(object):
    def video_directory_path(instance, filename):
        return 'video/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class Image_directory_path(object):
    def image_directory_path(instance, filename):
        return 'images/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

## Classes for advertising users
class Video_directory_path_commercial(object):
    def video_directory_path(instance, filename):
        return 'video/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

## Classes for advertising users
class Image_directory_path_commercial(object):
    def image_directory_path(instance, filename):
        return 'images/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class Post(models.Model):
    ## contributor (of written material)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='User')
    title  = models.CharField('Title', max_length=55, validators=[has_no_singlequote], blank=True)
    tags = TaggableManager(blank=True)
    text = models.TextField('Text', max_length=1500)
    ## social link
    web_link = models.URLField('WebLink', blank=True)
    twitter_link = models.URLField('TwitterLink', blank=True)
    instagram_link = models.URLField('InstagramLink', blank=True)
    ## Date Data
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    ## Access level settings
    ## Public or private?
    access_level = models.CharField('Public/Private', max_length=10, choices=[(level.name, level.value) for level in AccessLevelChoice], default='public')
    pin_x = models.FloatField()
    pin_y = models.FloatField()
    objects = PostQuerySet.as_manager()
    ## Counting the number of times seen
    watched_count = models.PositiveIntegerField(default=0)
    favorite = models.ManyToManyField(User, related_name='Favorite', default=None, blank=True)
    like = models.ManyToManyField(User, related_name='Like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    dislike = models.ManyToManyField(User, related_name='DisLike', default=None, blank=True)
    dislike_count = models.BigIntegerField(default='0')
    bookmark_count = models.BigIntegerField(default='0')
    comment_count = models.BigIntegerField(default='0')
    country = models.CharField(default='', max_length=20)
    prefecture = models.CharField(default='', max_length=20)
    city = models.CharField(default='', max_length=50)
    ## Advertisement submission or not.
    commercial = models.CharField(default='None', max_length=5)
    ## Rough advertising genres
    food = models.CharField(default='None', max_length=5)
    shop = models.CharField(default='None', max_length=5)
    service = models.CharField(default='None', max_length=5)
    ## Tentative submission or not.
    provisional = models.CharField(default='No', max_length=5)
    ## Emotional Choice
    emotion = models.CharField('Emotion', default='Happy', max_length=10)
    ## Emotional Color
    color = models.CharField('Color', default='Happy', max_length=10)
    ## User Choice Emotion

    def update(self):
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def increment_watched_count(self):
        self.watched_count += 1
        self.update()

    def increment_comment_count(self):
        self.comment_count += 1
        self.update()

    def increment_bookmark_count(self):
        self.bookmark_count += 1
        self.update()

    def decrement_bookmark_count(self):
        self.bookmark_count -= 1
        self.update()

    def wrapper(self, *args, **kwargs):
        return

## Allow and save 3 images to be submitted.
class PostImage(models.Model):
    image = VersatileImageField(
        'PostImage',
        upload_to=Image_directory_path.image_directory_path,
        blank=True,
        null=True,
        validators=[MaxSizeValidator(100048)]
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def update(self):
        self.save()

    @property
    def thumbnail_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['600x600'].url

    @property
    def thumbnail_100_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['100x100'].url

    ## Reduce the size of the image and save it.
    def save(self, *args, **kwargs):
        super(PostImage, self).save(*args, **kwargs)
        temp_icon_name = self.image.name
        if self.image.width > 405 or self.image.height > 405:
            new_width = 405
            new_height = 405
            resized = get_thumbnail(self.image, "{}x{}".format(new_width, new_height))
            name = resized.name.split('/')[-1]
            self.image.save(name, ContentFile(resized.read()), True)
            try:
                delete(temp_icon_name)
            except TypeError:
                pass

    def wrapper(self, *args, **kwargs):
        return

## Comment model to the post.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='CommentUser')
    comment_text = models.TextField('CommentText', max_length=140, validators=[has_no_singlequote])
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Post')
    created_at = models.DateTimeField(default=timezone.now)
    like = models.ManyToManyField(User, related_name='CommentLike', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    dislike = models.ManyToManyField(User, related_name='CommentDisLike', default=None, blank=True)
    dislike_count = models.BigIntegerField(default='0')

    def __str__(self):
        return self.comment_text

## Video Submission
class VideoPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='VideoUser')
    title = models.CharField('VideoTitle', max_length=55, validators=[
                             has_no_singlequote], blank=True)
    tags = TaggableManager(blank=True)
    text = models.TextField('VideoText', max_length=1500)
    video = models.FileField(upload_to=Video_directory_path.video_directory_path,
                             blank=True, validators=[MaxSizeValidator(100048)])
    like = models.ManyToManyField(
        User, related_name='VideoLike', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    dislike = models.ManyToManyField(
        User, related_name='VideoDisLike', default=None, blank=True)
    dislike_count = models.BigIntegerField(default='0')
    bookmark_count = models.BigIntegerField(default='0')
    created_at = models.DateTimeField(default=timezone.now)
    prefecture = models.CharField(default='', max_length=20)
    city = models.CharField(default='', max_length=20)
    pin_x = models.FloatField()
    pin_y = models.FloatField()
    ## Emotional Choice
    emotion = models.CharField('VideoEmotion', default='Happy', max_length=10)
    ## Emotional Color
    color = models.CharField('VideoColor', default='Happy', max_length=10)

## Tie emotions without permission.
## It would be interesting to be able to search by the emotion people put on it.
class UserChoiceEmotionForPost(models.Model):
    ## I don't want it to be duplicated.
    def_emotion = models.CharField('def_emotion', max_length=150, unique=True)
    def_emotion_color = models.CharField('def_emotion', max_length=150, unique=True)
    own = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, related_name='Own')
    supporter = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='Supporter', blank=True)
    supporter_num = models.IntegerField(default=0)
    post = models.ManyToManyField(Post, related_name='PostEmotion')

    def __str__(self):
        return self.own.username

## I want to put emotion on it.
## Discover unseen emotions.
class CreatedEmotion(models.Model):
    new_emotion = models.CharField('new_emotion', max_length=150, unique=True)
    ## Must be color coded.
    new_emotion_color = models.CharField(
        'new_emotion_color', max_length=100, unique=True, blank=True)
    emotion_maker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='EmotionMaker')
    supporter = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='SupporterCreated')

    def __str__(self):
        return self.new_emotion
