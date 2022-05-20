from django import forms

## Simple Problem Report Form
class ContactForm(forms.Form):
   name = forms.CharField(label='お名前', max_length=50)
   email = forms.EmailField(label='メールアドレス',)
   message = forms.CharField(label='メッセージ', widget=forms.Textarea)
   myself = forms.BooleanField(label='内容を受け取る', required=False)