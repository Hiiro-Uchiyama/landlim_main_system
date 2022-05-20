from django import forms
from .models import Post, Tag, Comment
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

class PostAddForm(forms.ModelForm):
   class Meta:
      model = Post
      fields = ['title', 'text', 'image', 'tag']
      text = forms.CharField(widget = SummernoteWidget())

class CmtForm(forms.ModelForm):
   class Meta:
      model = Comment
      fields = ['text', 'username', 'email', 'web']