from django import forms
from .models import WantToDo
from django.forms import ModelForm

class WantToDoAddForm(forms.ModelForm):
   class Meta:
      model = WantToDo
      fields = ['want_todo_title', 'want_todo_text', 'pin_x', 'pin_y']