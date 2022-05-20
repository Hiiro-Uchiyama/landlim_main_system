from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from core.utils import build_absolute_uri, make_email_body_with_template

def send_password_reset_email(context, to_email_address):
    reset_url = build_absolute_uri(
        reverse(
            'accounts:reset-password-confirm',
            kwargs={'uidb64': context['uid'], 'token': context['token']}))
    url = reset_url.replace('http://https:', 'https://trade-container.herokuapp.com')

    send_mail('LandLim password reset email. LandLimパスワード再設定メール',
        make_email_body_with_template("If you would like to reset your password, please access the following URL.\n" + "パスワードの再設定をご希望の場合は下記のURLにアクセスしてください。 \n" + url),
        settings.DEFAULT_FROM_EMAIL,
        [to_email_address], fail_silently=False)

def send_accounts_activation_email(context, to_email_address):
    activation_url = build_absolute_uri(
        reverse(
            'accounts:activation',
            kwargs={'uidb64': context['uid'], 'token': context['token']}))
    url = activation_url.replace('http://https:', 'https://trade-container.herokuapp.com')

    send_mail('Notice of completion of LandLim temporary registration. LandLim仮登録完了のお知らせ',
        make_email_body_with_template("Thank you for registering with LandLim.\n" + "LandLimにご登録いただきありがとうございます。\n" + "By accessing the following URL, you will be able to complete this registration and log in.\n" + "下記のURLにアクセスすることで本登録完了となりログインが可能になります。\n" + url),
        settings.DEFAULT_FROM_EMAIL,
        [to_email_address], fail_silently=False)