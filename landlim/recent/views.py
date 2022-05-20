from django.shortcuts import render, get_object_or_404, redirect
from post.models import Post, PostImage
from post.utils import get_public_post_list, fetch_latest_sold_timeline
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

def is_valid_q(q):
    return q != '' and q is not None

## Checks are performed by referencing the user's location and the location of the post.
def recent(request):
    MAX_NUM_LATEST_POST = 50000
    latest_posts = get_public_post_list(
        Post.objects.all().order_by('-created_at')[:MAX_NUM_LATEST_POST])
    post_landlim = fetch_latest_sold_timeline()
    post = post_landlim[:50000]
    return render(request, 'recent/recent_timeline.html', {'post': latest_posts, 'landlim_post': post})

@login_required
def local_map(request):
    MAX_NUM_LATEST_POST = 50000
    latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at')[:MAX_NUM_LATEST_POST])
    if request.user.city:
        user_city = request.user.city
        post_landlim = fetch_latest_sold_timeline()
        post = post_landlim[:50000]
        local_posts = get_public_post_list(Post.objects.all().filter(prefecture=user_city).order_by('-created_at')[:MAX_NUM_LATEST_POST])
        return render(request, 'recent/local_map.html', {'post': latest_posts, 'landlim_post': post, 'local_post': local_posts})
    else:
        messages.add_message(request, messages.ERROR, _("Please add your country and city information in Edit Account"))
        post_landlim = fetch_latest_sold_timeline()
        post = post_landlim[:50000]
        return render(request, 'recent/local_map.html', {'post': latest_posts, 'landlim_post': post})

@login_required
def recent_video(request):
    MAX_NUM_LATEST_POST = 50000
    latest_posts = get_public_post_list(
        Post.objects.all().order_by('-created_at')[:MAX_NUM_LATEST_POST])
    post_landlim = fetch_latest_sold_timeline()
    post = post_landlim[:50000]
    return render(request, 'recent/recent_video.html', {'post': latest_posts, 'landlim_post': post})
