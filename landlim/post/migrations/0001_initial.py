# Generated by Django 3.2.6 on 2022-03-08 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_file_validator.validators
import post.models
import taggit.managers
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=140, validators=[post.models.has_no_singlequote], verbose_name='CommentText')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('like_count', models.BigIntegerField(default='0')),
                ('dislike_count', models.BigIntegerField(default='0')),
                ('dislike', models.ManyToManyField(blank=True, default=None, related_name='CommentDisLike', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, default=None, related_name='CommentLike', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=55, validators=[post.models.has_no_singlequote], verbose_name='Title')),
                ('text', models.TextField(max_length=1500, verbose_name='Text')),
                ('web_link', models.URLField(blank=True, verbose_name='WebLink')),
                ('twitter_link', models.URLField(blank=True, verbose_name='TwitterLink')),
                ('instagram_link', models.URLField(blank=True, verbose_name='InstagramLink')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('access_level', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10, verbose_name='Public/Private')),
                ('pin_x', models.FloatField()),
                ('pin_y', models.FloatField()),
                ('watched_count', models.PositiveIntegerField(default=0)),
                ('like_count', models.BigIntegerField(default='0')),
                ('dislike_count', models.BigIntegerField(default='0')),
                ('bookmark_count', models.BigIntegerField(default='0')),
                ('comment_count', models.BigIntegerField(default='0')),
                ('country', models.CharField(default='', max_length=20)),
                ('prefecture', models.CharField(default='', max_length=20)),
                ('city', models.CharField(default='', max_length=50)),
                ('commercial', models.CharField(default='None', max_length=5)),
                ('food', models.CharField(default='None', max_length=5)),
                ('shop', models.CharField(default='None', max_length=5)),
                ('service', models.CharField(default='None', max_length=5)),
                ('provisional', models.CharField(default='No', max_length=5)),
                ('emotion', models.CharField(default='Happy', max_length=10, verbose_name='Emotion')),
                ('color', models.CharField(default='Happy', max_length=10, verbose_name='Color')),
                ('dislike', models.ManyToManyField(blank=True, default=None, related_name='DisLike', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank=True, default=None, related_name='Favorite', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, default=None, related_name='Like', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=55, validators=[post.models.has_no_singlequote], verbose_name='VideoTitle')),
                ('text', models.TextField(max_length=1500, verbose_name='VideoText')),
                ('video', models.FileField(blank=True, upload_to=post.models.Video_directory_path.video_directory_path, validators=[django_file_validator.validators.MaxSizeValidator(10048)])),
                ('like_count', models.BigIntegerField(default='0')),
                ('dislike_count', models.BigIntegerField(default='0')),
                ('bookmark_count', models.BigIntegerField(default='0')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('prefecture', models.CharField(default='', max_length=20)),
                ('city', models.CharField(default='', max_length=20)),
                ('pin_x', models.FloatField()),
                ('pin_y', models.FloatField()),
                ('emotion', models.CharField(default='Happy', max_length=10, verbose_name='VideoEmotion')),
                ('color', models.CharField(default='Happy', max_length=10, verbose_name='VideoColor')),
                ('dislike', models.ManyToManyField(blank=True, default=None, related_name='VideoDisLike', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, default=None, related_name='VideoLike', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='VideoUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserChoiceEmotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('def_emotion', models.CharField(max_length=150, verbose_name='def_emotion')),
                ('supporter_num', models.IntegerField()),
                ('comment', models.ManyToManyField(related_name='CommentEmotion', to='post.Comment')),
                ('own', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Own', to=settings.AUTH_USER_MODEL)),
                ('post', models.ManyToManyField(related_name='PostEmotion', to='post.Post')),
                ('supporter', models.ManyToManyField(related_name='Supporter', to=settings.AUTH_USER_MODEL)),
                ('video_post', models.ManyToManyField(related_name='VideoPostEmotion', to='post.VideoPost')),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=post.models.Image_directory_path.image_directory_path, validators=[django_file_validator.validators.MaxSizeValidator(100048)], verbose_name='PostImage')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
        migrations.CreateModel(
            name='CreatedEmotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_emotion', models.CharField(max_length=150, unique=True, verbose_name='new_emotion')),
                ('new_emotion_color', models.CharField(max_length=100, unique=True, verbose_name='new_emotion_color')),
                ('emotion_maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EmotionMaker', to=settings.AUTH_USER_MODEL)),
                ('supporter', models.ManyToManyField(related_name='SupporterCreated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Post', to='post.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CommentUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
