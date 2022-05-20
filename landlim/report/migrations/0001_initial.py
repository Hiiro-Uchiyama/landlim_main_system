# Generated by Django 3.2.6 on 2022-03-08 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55, verbose_name='ReportTitle')),
                ('text', models.CharField(max_length=150, verbose_name='ReportText')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('report', models.ManyToManyField(blank=True, to='post.Post', verbose_name='Report')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReportUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]