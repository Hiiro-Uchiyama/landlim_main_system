from django.shortcuts import render, get_object_or_404, redirect
from post.models import Post, PostImage
from blog.models import Post as BlogPost
from blog.models import Comment as BlogComment
from blog.models import Category as BlogCategory
from blog.models import Tag as BlogTag
from recruit.models import Post as RecruitPost
from recruit.models import Category as RecruitCategory
from recruit.models import Tag as RecruitTag
from post.utils import get_public_post_list, fetch_latest_sold_timeline
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

def is_valid_q(q):
    return q != '' and q is not None

@login_required
def index(request):
    MAX_NUM_LATEST_POST = 50000
    latest_posts = get_public_post_list(Post.objects.all().filter(commercial='None').order_by('-created_at')[:MAX_NUM_LATEST_POST])
    post_landlim = fetch_latest_sold_timeline()
    post = post_landlim[:50000]
    ## Obtain paid contributions.
    commercial = Post.objects.all().filter(commercial='True').order_by('-created_at')
    food = Post.objects.all().filter(commercial='True', food='True').order_by('-created_at')
    shop = Post.objects.all().filter(commercial='True', shop='True').order_by('-created_at')
    service = Post.objects.all().filter(commercial='True', service='True').order_by('-created_at')
    blog = BlogPost.objects.all()
    ## Whether the message is acceptable to the user.
    if request.user.want_messages == 'yes':
        messages.add_message(request, messages.SUCCESS, _("If you are unable to retrieve your location, please review your location settings."))
        messages.add_message(request, messages.SUCCESS, _("No problem! Even if you can't use your location, you can still have fun with Search and TimeLine from the sidebar."))
    if request.user.city:
        commercial_post = Post.objects.all().filter(commercial='True', prefecture=request.user.city).order_by('-like_count')[:3]
        return render(request, 'core/index.html', {'post': latest_posts, 'landlim_post': post, 'commercial': commercial, 'food': food, 'shop': shop, 'service': service, 'commercial_post': commercial_post, 'blog': blog})
    else:
        good_post = get_public_post_list(Post.objects.all().filter(commercial='None').order_by('-like_count'))[:3]
        return render(request, 'core/index.html', {'post': latest_posts, 'landlim_post': post, 'commercial': commercial, 'food': food, 'shop': shop, 'service': service, 'good_post': good_post, 'blog': blog})

## As for the developer blog, I will keep it updated.
def first(request):
    return render(request, 'core/front_page.html')
