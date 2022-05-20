from __future__ import unicode_literals
from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class WantToDo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='WantToDoUser')
    want_todo_title = models.CharField('WantToDoTitle', max_length=100)
    want_todo_text = models.CharField('WantToDoText', max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    pin_x = models.FloatField()
    pin_y = models.FloatField()
    ## the other party
    checked = models.BooleanField('is_Check', default=None)
    ## Finished todo list
    finished = models.BooleanField('is_Finished', default=None)

    def __str__(self):
        return self.want_todo_text

class WantToDoPoint(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='WantToDoUserPoint')
    point = models.FloatField(default=0)

    def __str__(self):
        return self.point