import re
from . import emails
from django import forms
from django.conf import settings
from .models import User
from django.contrib.auth import forms as django_forms, update_session_auth_hash
from django.utils.translation import gettext_lazy as _

class SignupForm(django_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email

    def clean(self):
        cleaned_data=super(SignupForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")
        if password != confirm_password:
            raise forms.ValidationError("パスワードが一致しませんでした。パスワードを入力し直してください。")

class LoginForm(django_forms.AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].label = "Email address or user name. メールアドレスまたはユーザ名"
        if request:
            email = request.GET.get('email')
            if email:
                self.fields['username'].initial = email

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        email = username_or_email
        try:
            user = User.objects.get(email=email)
            if user:
                self.cleaned_data['username'] = user.username
        except:
            raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        super().clean()

## If there are any missing fields, add them back in.
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        ## There was an error here.
        fields = ('icon', 'background', 'description', 'nickname', 'hobby', 'web_link',
                  'twitter_link', 'instagram_link', 'facebook_link', 'want_messages', 'country', 'prefecture', 'city', 'emotion', 'color')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = forms.FileInput()
        self.fields['icon'].widget.attrs={'style':'display:none;', 'id':'icon' , 'onchange': 'fileget(this,\'0\');', }
        self.fields['background'].widget = forms.FileInput()
        self.fields['background'].widget.attrs={'style':'display:none;', 'id':'background' , 'onchange': 'fileget(this,\'0\');', }

## Password Change Form
class ChangePasswordForm(django_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].user = self.user
        self.fields['old_password'].widget.attrs['placeholder'] = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = ''
        del self.fields['new_password2']

def logout_on_password_change(request, user):
    if (update_session_auth_hash is not None and
            not settings.LOGOUT_ON_PASSWORD_CHANGE):
        update_session_auth_hash(request, user)

## Password Reset Form
class PasswordResetForm(django_forms.PasswordResetForm):
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email:
            users = User.objects.filter(email=email)
            if not users or not users[0].is_active:
                self._errors["email"]=[_("The account for that email address does not exist or has not been registered")]

    def get_users(self, email):
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return active_users

    def send_mail(
            self, subject_template_name, email_template_name, context,
            from_email, to_email, html_email_template_name=None):
        del context['user']
        emails.send_password_reset_email(context, to_email)

## Enter your password to clear your account.
class DeleteAccountsForm(forms.Form):
    password = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
    def is_valid(self, user):
        if super().is_valid():
            if not user.check_password(self.cleaned_data['password']):
                self._errors["password"] = [_("Please enter the correct password")]
            else:
                return True
        return False

class GetYourPositionForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ('pin_x', 'pin_y')