from xml.etree.ElementTree import Comment
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from post.models import Post, Comment, VideoPost

class Notion(models.Model):
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='NotionReceiverUser')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='NotionUser')
    notion_title = models.CharField('NotionTitle', max_length=100)
    notion_text = models.CharField('NotionPost', max_length=200)
    notion_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    notion_video = models.ForeignKey(VideoPost, on_delete=models.CASCADE, blank=True, null=True)
    notion_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.notion_title
