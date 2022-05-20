# Generated by Django 3.2.12 on 2022-03-15 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_file_validator.validators
import post.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChoiceEmotionForPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('def_emotion', models.CharField(max_length=150, unique=True, verbose_name='def_emotion')),
                ('def_emotion_color', models.CharField(max_length=150, unique=True, verbose_name='def_emotion')),
                ('supporter_num', models.IntegerField(default=0)),
                ('own', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Own', to=settings.AUTH_USER_MODEL)),
                ('post', models.ManyToManyField(related_name='PostEmotion', to='post.Post')),
                ('supporter', models.ManyToManyField(blank=True, related_name='Supporter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='createdemotion',
            name='new_emotion_color',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='new_emotion_color'),
        ),
        migrations.AlterField(
            model_name='videopost',
            name='video',
            field=models.FileField(blank=True, upload_to=post.models.Video_directory_path.video_directory_path, validators=[django_file_validator.validators.MaxSizeValidator(100048)]),
        ),
        migrations.DeleteModel(
            name='UserChoiceEmotion',
        ),
    ]