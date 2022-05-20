from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import User

## Validators are needed for critical items.
def has_no_singlequote(value):
    if "\'" in value:
        raise ValidationError(
            'Do not include single quotes (\')',
            params={'value': value},
        )

## Variable messages to be output on the template.
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='AdminUser')
    message_title = models.CharField('MessageTitle', max_length=140, validators=[has_no_singlequote])
    message_text = models.CharField('MessageText', max_length=140, validators=[has_no_singlequote])
    created_at = models.DateTimeField(default=timezone.now)
    reach_user = models.ManyToManyField(User, related_name='Reach_user')
    web_url = models.URLField('WebLink', blank=True)

    def __str__(self):
        return self.message_text

## Testing the Rest Framework.
class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()

class Entry(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLIC = "public"
    STATUS_SET = (
            (STATUS_DRAFT, "下書き"),
            (STATUS_PUBLIC, "公開中"),
    )
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=STATUS_SET, default=STATUS_DRAFT, max_length=8)
    author = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE)
