from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post as RecruitPost
from .models import Tag as RecruitTag
from .models import Category as RecruitCategory
from .forms import PostAddForm, EasyApplyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from search_recruit.views import *
from search_post.forms import *

def is_valid_q(q):
    return q != '' and q is not None

def recruit(request):
    posts = RecruitPost.objects.all().order_by('-created_at')
    title_or_user = request.GET.get('title_or_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    tag = request.GET.get('tag')
    page_obj = paginate_query(request, posts, settings.PAGE_PER_ITEM)
    recent_post = RecruitPost.objects.all().order_by('-created_at')[:5]
    recent_image = RecruitPost.objects.all().order_by('created_at')[:5]
    tags = RecruitTag.objects.all()
    category = RecruitCategory.objects.all()
    if is_valid_q(title_or_user):
        posts = posts.filter(Q(title__icontains=title_or_user)
                                | Q(user__username__icontains=title_or_user)
                                ).distinct()
    if is_valid_q(date_min):
        posts = posts.filter(created_at__gte=date_min)
    if is_valid_q(date_max):
        posts = posts.filter(created_at__lt=date_max)
    if is_valid_q(tag) and tag != 'Select a tag...':
        posts = posts.filter(tag__tag=tag)
    if request.method == "GET":
        keyword_form = SearchPostKeywordForm(request.GET)
        latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at')[:20])
        if keyword_form.is_valid():
            search_results = get_public_post_list(search(request))
            if len(search_results) > 0:
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_recruit_by_title.html', {'latest_post_list': latest_posts, 'post_list': search_results, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
            else:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "You might want to try changing to a keyword with a larger population.")
                return render(request, 'search/search_recruit_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
    if request.method == "GET":
        q = request.GET.get('q_tag')
        tag_form = SearchPostTagForm(request.GET)
        if q:
          try:
            tag = RecruitTag.objects.get(tag=q)
          except:
            tag = False
            latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at')[:20])
          if tag:
            latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at').filter(tag=tag)[:10])
        else:
            latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at')[:20])
        if tag_form.is_valid():
            try:
                tag = RecruitTag.objects.get(tag=q)
                post_list = get_public_post_list(RecruitPost.objects.filter(tag=tag))
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_recruit_by_tag.html', {'latest_post_list': latest_posts, 'post_list': post_list, 'tag_form': tag_form, 'is_searched': True, 'tags': tags, 'category': category})
            except:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "Discover the tags that interest you in our tag list!")
                messages.add_message(request, messages.SUCCESS, "However, there are cases where only tags are present")
                return render(request, 'search/search_recruit_by_tag.html', {'latest_post_list': latest_posts, 'tag_form': tag_form, 'is_searched': True, 'tags': tags, 'category': category})
    tag_form = SearchPostTagForm()
    keyword_form = SearchPostKeywordForm()
    return render(request, 'recruit/recruit.html',
                    {'posts': posts, 'title_or_user': title_or_user, 'date_min': date_min, 'date_max': date_max, 'tag': tag, 'page_obj': page_obj, 'recent_post': recent_post, 'recent_image': recent_image, 'tags': tags, 'category': category})

def detail(request, post_id):
    post = get_object_or_404(RecruitPost, id=post_id)
    liked = False
    tag = post.tag
    recent_post = RecruitPost.objects.all().filter(tag=tag)
    tags = RecruitTag.objects.all()
    category = RecruitCategory.objects.all()
    if request.method == "GET":
        keyword_form = SearchPostKeywordForm(request.GET)
        latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at')[:20])
        if keyword_form.is_valid():
            search_results = get_public_post_list(search(request))
            if len(search_results) > 0:
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_recruit_by_title.html', {'latest_post_list': latest_posts, 'post_list': search_results, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
            else:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "You might want to try changing to a keyword with a larger population.")
                return render(request, 'search/search_recruit_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
    keyword_form = SearchPostKeywordForm()
    if request.method == "GET":
        q = request.GET.get('q_tag')
        print(q)
        tag_form = SearchPostTagForm(request.GET)
        if tag_form.is_valid():
            if q:
                try:
                    tag = RecruitTag.objects.get(tag=q)
                except:
                    tag = False
                    latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at')[:20])
                if tag:
                    latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at').filter(tag=tag)[:10])
                else:
                    latest_posts = get_public_post_list(RecruitPost.objects.all().order_by('-created_at')[:20])
            try:
                tag = RecruitTag.objects.get(tag=q)
                post_list = get_public_post_list(RecruitPost.objects.filter(tag=tag))
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_recruit_by_tag.html', {'latest_post_list': latest_posts, 'post_list': post_list, 'tag_form': tag_form, 'is_searched': True, 'tags': tags, 'category': category})
            except:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "Discover the tags that interest you in our tag list!")
                messages.add_message(request, messages.SUCCESS, "However, there are cases where only tags are present")
                return render(request, 'search/search_recruit_by_tag.html', {'latest_post_list': latest_posts, 'tag_form': tag_form, 'is_searched': True, 'tags': tags, 'category': category})
    tag_form = SearchPostTagForm()
    return render(request, 'recruit/details.html', {'post': post, 'tag_form': tag_form, 'liked': liked, 'recent_post': recent_post, 'tags': tags, 'category': category})

def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

class PostArchiveMixin:
    model = RecruitPost
    paginate_by = 10
    date_field = 'created_at'
    template_name = 'blog/post_list.html'
    allow_empty = True
    make_object_list = True


def easy_apply(request, user_id):
    if request.method == 'POST':
        form = EasyApplyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phoneNumber = form.cleaned_data['phoneNumber']
            user = User.objects.filter(user_id=user_id)
            recipients = user.email
            try:
                send_mail(name, text, email, recipients)
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            messages.add_message(request, messages.SUCCESS, _("Your enquiry has been sent to LandLim"))
            return render(request, 'recruit/apply/post_apply_success.html')
    else:
        form = EasyApplyForm()
    return render(request, 'recruit/apply/post_apply.html', {'form': form})

class PostArchiveIndex(PostArchiveMixin, generic.ArchiveIndexView):
    pass

class PostYearArchiveIndex(PostArchiveMixin, generic.YearArchiveView):
    pass

class PostMonthArchiveIndex(PostArchiveMixin, generic.MonthArchiveView):
    month_format = '%m'

class PostDetail(generic.DetailView):
    model = RecruitPost

class PostList(generic.ListView):
    model = RecruitPost

class PostDetail(generic.DetailView):
    model = RecruitPost

def tag_list(request):
    tags = RecruitTag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})

def tag_linked_post(request, tag_id):
    tags = RecruitTag.objects.all()
    tag = RecruitTag.objects.filter(id=tag_id)
    post_list = RecruitPost.objects.filter(tag=tag)
    return render(request, 'blog/tag_linked_post.html', {'post_list': post_list, 'tags': tags, 'tag': tag})

def category_list(request):
    categories = RecruitCategory.objects.all()
    return render(request, 'blog/tag_list.html', {'categories': categories})

def category_linked_post(request, category_id):
    categories = RecruitCategory.objects.all()
    category = RecruitCategory.objects.filter(id=category_id)
    post_list = RecruitPost.objects.filter(category=category)
    return render(request, 'blog/tag_linked_post.html', {'post_list': post_list, 'categories': categories, 'category': category})
