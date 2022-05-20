import re
from traceback import print_exc
from .models import User
from django.conf import settings
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignupForm, LoginForm, UserEditForm, ChangePasswordForm, PasswordResetForm, logout_on_password_change, DeleteAccountsForm, GetYourPositionForm
## Not yet installed.
## from trade_app.rating.models import UserRating
## from trade_app.notification.models import Notification
from copy import deepcopy
from post.models import Comment, Post
from post.views import post_details
from post.utils import get_public_post_list
from .emails import send_accounts_activation_email
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
## Not yet installed.
## from todolist.utils import get_undone_todo_list, get_done_todo_list
## from notification.utils import fetch_notification_list

## How about official users and high user level people being found by search?
## Make a simple search form.

## Shouldn't you be able to change your email address or password?

def signup_accounts(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            context = {'uid': uidb64, 'token': token}
            to_email_address = user.email
            send_accounts_activation_email(context, to_email_address)
            messages.success(request, (_('Your temporary registration is now complete!')))
            messages.success(request, (_('You will have received a URL to activate your account at your registered email address.')))
            redirect_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
            return redirect(redirect_url)
        else:
            messages.error(request, (_('Is there a problem with my password confirmation or email address?')))
            messages.error(request, (_('The username must be a unique username')))
            messages.error(request, (_('By the way, you can also register with a Google account etc.')))
    ctx = {'form': form}
    return render(request, 'accounts/signup_accounts.html', ctx)

def login_accounts(request, backends='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        redirect_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        return redirect(redirect_url)
    kwargs = {
        'template_name': 'accounts/login_accounts.html',
        'authentication_form': LoginForm}
    return auth_views.LoginView.as_view(**kwargs)(request, **kwargs)

## I have some reservations about this.
def user_level(liked_num):
    if liked_num < 100:
        return "Bronze"
    elif liked_num < 1000:
        return "Silver"
    elif liked_num < 10000:
        return "Gold"
    elif liked_num < 100000:
        return "Platinum"
    elif liked_num < 1000000:
        return "Black"
    elif 10000 <= liked_num:
        return "Master"
    else:
        return "???"

@login_required
def own_page(request):
    my_info = User.objects.filter(username=request.user)
    own_post_list = Post.objects.filter(user=request.user)
    own_image_url = []
    own_post_num = len(own_post_list)
    own_post_is_liked_num = 0
    for i in own_post_list:
        own_post_is_liked_num += i.like_count
    own_level = user_level(own_post_is_liked_num)
    for own_post_image in own_post_list:
        if own_post_image.postimage_set.first():
            if own_post_image.postimage_set.first().thumbnail_url:
                own_image_url.append(own_post_image.postimage_set.first().thumbnail_url)
    return render(request, 'accounts/own_page.html', {'my_info': my_info, 'own_post_list': own_post_list, 'own_image_url': own_image_url, 'own_post_num': own_post_num, 'own_post_is_liked_num': own_post_is_liked_num, 'own_level': own_level})

@login_required
def others_page(request, user_pk):
    others_user = get_object_or_404(User, pk=user_pk)
    others_user_post_list = get_public_post_list(Post.objects.filter(user=others_user))
    others_image_url = []
    others_user_post_num = len(others_user_post_list)
    others_user_follower_num = others_user.get_follower_num
    others_user_post_is_liked_num = 0
    for i in others_user_post_list:
        others_user_post_is_liked_num += i.like_count
    others_user_level = user_level(others_user_post_is_liked_num)
    for others_post_image in others_user_post_list:
        if others_post_image.postimage_set.first():
            if others_post_image.postimage_set.first().thumbnail_url:
                others_image_url.append(others_post_image.postimage_set.first().thumbnail_url)
    return render(request, 'accounts/others_page.html', {'others_user': others_user, 'others_user_post_list': others_user_post_list, "others_image_url": others_image_url, 'others_user_post_num': others_user_post_num, 'others_user_post_is_liked_num': others_user_post_is_liked_num, 'others_user_level': others_user_level, 'others_user_follower_num': others_user_follower_num})

@login_required
def logout_accounts(request):
    auth.logout(request)
    messages.success(request, (_('You have been logged out.')))
    messages.success(request, (_('Have a good day!')))
    return redirect(settings.LOGIN_REDIRECT_URL)

def activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, (_('Your registration is now complete!')))
        messages.success(request, (_('Welcome to LandLim')))
        messages.success(request, (_("Come and enjoy LandLim to your heart's content!")))
        return redirect('accounts:own_page')
    else:
        return HttpResponse("Activation link has expired")

def password_reset(request):
    kwargs = {
        'template_name': 'accounts/password_reset.html',
        'success_url': reverse_lazy('accounts:reset-password-done'),
        'form_class': PasswordResetForm}
    return auth_views.PasswordResetView.as_view(**kwargs)(request, **kwargs)

class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_from_key.html'
    success_url = reverse_lazy('accounts:reset-password-complete')
    token = None
    uidb64 = None

def password_reset_confirm(request, uidb64=None, token=None):
    kwargs = {
        'template_name': 'accounts/password_reset_from_key.html',
        'success_url': reverse_lazy('accounts:reset-password-complete'),
        'token': token,
        'uidb64': uidb64}
    return PasswordResetConfirm.as_view(**kwargs)(request, **kwargs)

def get_or_process_password_form(request):
    form = ChangePasswordForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        logout_on_password_change(request, form.user)
        messages.success(request, pgettext(
            _('LandLim has successfully changed your password!')))
    return form

@login_required
def edit_accounts(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, (_('Profile information has been changed.')))
            return render(request, 'accounts/own_page.html')
        else:
            for _field in form:
                for error in _field.errors:
                    messages.error(request, error,extra_tags=('danger'))
            return render(request, 'accounts/edit_accounts.html', {'form': form})
    form = UserEditForm(instance=request.user)
    return render(request, 'accounts/edit_accounts.html', {'form': form})

@login_required
def delete_accounts(request):
    if request.method == 'POST':
        form = DeleteAccountsForm(request.POST)
        user = User.objects.get(email=request.user.email)
        if form.is_valid(user):
            user.is_active = False
            user.is_cancel = "yes"
            user.save()
            messages.success(request, _('You have successfully withdrawn your membership'))
            messages.success(request, _('LandLim looks forward to welcoming you back!'))
            return redirect('accounts:login_accounts')
    else:
        form = DeleteAccountsForm()
    return render(request, 'accounts/delete_accounts.html', {'form': form})

@login_required
def like_list(request):
    user = request.user
    post = Post.objects.all().filter(like=user)
    return render(request, 'like/liked.html', {'post': post})

@login_required
def like_map(request):
    user = request.user
    post = Post.objects.all().filter(like=user)
    return render(request, 'like/liked_map.html', {'post': post})

@login_required
def following_list(request):
    user = request.user
    following_user = User.objects.filter(follower=user)
    return render(request, 'follow/following_list.html', {'user': following_user})

@login_required
def follower_list(request):
    user = request.user
    follower_user = User.objects.filter(following=user)
    return render(request, 'follow/follower_list.html', {'user': follower_user})

@login_required
def friends_map(request):
    user = request.user
    friends_post = []
    following_and_follower_user = User.objects.filter(following=user, follower=user)
    if following_and_follower_user:
        for i in following_and_follower_user:
            user_post = get_public_post_list(Post.objects.filter(user=i))
            for i_ in user_post:
                friends_post.append(i_)
    return render(request, 'friend/friends_map.html', {'friends_post': friends_post})

@login_required
def friends_timeline(request):
    user = request.user
    friends_post = []
    following_and_follower_user = User.objects.filter(following=user, follower=user)
    if following_and_follower_user:
        for i in following_and_follower_user:
            user_post = get_public_post_list(Post.objects.filter(user=i))
            for i_ in user_post:
                friends_post.append(i_)
    return render(request, 'friend/friends_timeline.html', {'friends_post': friends_post})

@login_required
def follow_unfollow(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('userid'))
        user = get_object_or_404(User, pk=pk)
        print(user.follower_count)
        if user.follower.filter(id=request.user.id).exists():
            user.follower.remove(request.user)
            request.user.following.remove(user)
            user.follower_count -= 1
            result = user.follower_count
            user.save()
        else:
            user.follower.add(request.user)
            request.user.following.add(user)
            user.follower_count += 1
            result = user.follower_count
            user.save()
        return JsonResponse({'result': result})

@login_required
def block_unblock(request):
    if request.POST.get('action') == 'post':
        result = ''
        blocked = 'Blocked'
        unblock = 'Unblocked'
        pk = int(request.POST.get('userid'))
        user = get_object_or_404(User, pk=pk)
        if request.user.block.filter(id=user.id).exists():
            request.user.block.remove(user)
            user.save()
            result = unblock
        else:
            user.follower.add(request.user)
            request.user.block.add(user)
            user.save()
            result = blocked
        return JsonResponse({'result': result})

## Apparently, it cannot be saved.
@login_required
def get_your_position(request):
    user = request.user
    if request.method == 'POST':
        form = GetYourPositionForm(request.POST,instance=user)
        if form.is_valid():
            pin_x = request.POST.get("pin_x")
            pin_y = request.POST.get("pin_y")
            user.pin_x = pin_x
            user.pin_y = pin_y
            user.save()
            messages.success(request, (_('Profile information has been changed.')))
            return render(request, 'accounts/own_page.html')
        else:
            for _field in form:
                for error in _field.errors:
                    messages.error(request, error,extra_tags=('danger'))
            return render(request, 'accounts/edit_accounts.html', {'form': form})
    form = GetYourPositionForm(instance=user)
    return render(request, 'accounts/get_your_position_form.html', {'form': form})
