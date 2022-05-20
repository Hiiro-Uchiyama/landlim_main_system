from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post as BlogPost, Tag
from .models import Comment as BlogComment
from .models import Category as BlogCategory
from .models import Tag as BlogTag
from .forms import PostAddForm, CmtForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from search_blog.views import *
from search_post.forms import *

def is_valid_q(q):
    return q != '' and q is not None

def blog(request):
    ## Basic information required for blog posting
    posts = BlogPost.objects.all().order_by('-created_at')
    title_or_user = request.GET.get('title_or_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    ## If there is a tag on the front side, get the tag.
    tag = request.GET.get('tag')
    ## Generating Pagination Objects
    page_obj = paginate_query(request, posts, settings.PAGE_PER_ITEM)
    ## Retrieve recent posts and recently posted images.
    recent_post = BlogPost.objects.all().order_by('-created_at')[:5]
    recent_image = BlogPost.objects.all().order_by('created_at')[:5]
    ## Retrieve all tags and categories.
    tags = BlogTag.objects.all()
    category = BlogCategory.objects.all()
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
    ## Invoking the GET method
    if request.method == "GET":
        ## Keyword Form Setup
        keyword_form = SearchPostKeywordForm(request.GET)
        ## Retrieve the 20 most recent posts.
        latest_posts = get_public_post_list(BlogPost.objects.all().order_by('-created_at')[:20])
        ## Validate the form.
        if keyword_form.is_valid():
            ## Perform a keyword search.
            search_results = get_public_post_list(search(request))
            ## Return search results if they exist.
            if len(search_results) > 0:
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'post_list': search_results, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
            else:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "You might want to try changing to a keyword with a larger population.")
                return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
    keyword_form = SearchPostKeywordForm()
    return  render(request, 'blog/blog.html',
                    {'posts': posts, 'title_or_user': title_or_user, 'date_min': date_min, 'date_max': date_max, 'tag': tag, 'page_obj': page_obj, 'recent_post': recent_post, 'recent_image': recent_image, 'tags': tags, 'category': category})

def detail(request, post_id):
    ## Retrieve the details of a given submission.
    ## Get more information about the blog.
    post = get_object_or_404(BlogPost, id=post_id)
    comments = BlogComment.objects.filter(post=post).order_by('-created_at')
    liked = False
    tag = post.tag
    recent_post = BlogPost.objects.all().filter(tag=tag)
    tags = BlogTag.objects.all()
    category = BlogCategory.objects.all()
    ## Activation of comment submission form by POST method
    if request.method == "POST":
        ## Comment Form Settings
        form = CmtForm(request.POST or None)
        if form.is_valid():
            ## Comments will be accepted.
            text = request.POST.get('text')
            username = request.POST.get('username')
            email = request.POST.get('email')
            web = request.POST.get('web')
            comment = BlogComment.objects.create(
                post=post, username=username, text=text, email=email, web=web)
            comment.save()
    else:
        form = CmtForm()
    ## The GET method makes the search system work.
    if request.method == "GET":
        ## Retrieve search keywords.
        keyword_form = SearchPostKeywordForm(request.GET)
        latest_posts = get_public_post_list(BlogPost.objects.all().order_by('-created_at')[:20])
        ## Search Form Validation
        if keyword_form.is_valid():
            search_results = get_public_post_list(search(request))
            if len(search_results) > 0:
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'post_list': search_results, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
            else:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "You might want to try changing to a keyword with a larger population.")
                return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'is_searched': True, 'tags': tags, 'category': category})
    keyword_form = SearchPostKeywordForm()
    return render(request, 'blog/details.html', {'post': post, 'form': form, 'tag_form': tag_form, 'comments': comments, 'liked': liked, 'recent_post': recent_post, 'tags': tags, 'category': category})

## Function to generate pagination
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
    model = BlogPost
    paginate_by = 10
    date_field = 'created_at'
    template_name = 'blog/post_list.html'
    allow_empty = True
    make_object_list = True

class PostArchiveIndex(PostArchiveMixin, generic.ArchiveIndexView):
    pass

class PostYearArchiveIndex(PostArchiveMixin, generic.YearArchiveView):
    pass

class PostMonthArchiveIndex(PostArchiveMixin, generic.MonthArchiveView):
    month_format = '%m'

class PostDetail(generic.DetailView):
    model = BlogPost

class PostList(generic.ListView):
    model = BlogPost

class PostDetail(generic.DetailView):
    model = BlogPost

## Get a list of tags
def tag_list(request):
    tags = BlogTag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})

## Retrieve posts tied to a tag
def tag_linked_post(request, tag_id):
    tags = BlogTag.objects.all()
    tag = BlogTag.objects.filter(id=tag_id)
    post_list = BlogPost.objects.filter(tag=tag)
    return render(request, 'blog/tag_linked_post.html', {'post_list': post_list, 'tags': tags, 'tag': tag})

## Get a list of categories
def category_list(request):
    categories = BlogCategory.objects.all()
    return render(request, 'blog/tag_list.html', {'categories': categories})

## Retrieve posts tied to a category
def category_linked_post(request, category_id):
    categories = BlogCategory.objects.all()
    category = BlogCategory.objects.filter(id=category_id)
    post_list = BlogPost.objects.filter(category=category)
    return render(request, 'blog/tag_linked_post.html', {'post_list': post_list, 'categories': categories, 'category': category})
