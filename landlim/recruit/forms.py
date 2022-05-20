from django import forms
from .models import Post, Tag, EasyApply
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

class PostAddForm(forms.ModelForm):
   class Meta:
      model = Post
      fields = ['title', 'text', 'image', 'tag']
      text = forms.CharField(widget = SummernoteWidget())

class EasyApplyForm(forms.ModelForm):
   class Meta:
      model = EasyApply
      fields = ['subject', 'text', 'username', 'email', 'phoneNumber']