from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post as BlogPost
from search_post.forms import SearchPostKeywordForm, SearchPostOptionForm, SearchPostTagForm, SearchPostCouForm, SearchPostPreForm, SearchPostEmoForm
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from post.utils import get_public_post_list
from django.views.generic.list import ListView
from blog.models import Tag as BlogTag
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

## Complementary to the submission.
def api_posts_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'name': str(post[0])} for post in list(
            BlogPost.objects.distinct().values_list('title').filter(title__icontains=keyword))]
    else:
        post_list = []
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_tags_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        tag_list = [{'name': str(tags[0])} for tags in list(
            BlogTag.objects.distinct().values_list('name').filter(name__icontains=keyword))]
    else:
        tag_list = []
    return JsonResponse({'object_list': tag_list})

## Complementary to the submission.
def api_cou_get(request):
    post_list = [{'name': str(post[0])} for post in list(
        BlogPost.objects.distinct().values_list('country').order_by('country'))]
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_pre_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'name': str(post[0])} for post in list(BlogPost.objects.distinct(
        ).values_list('prefecture').filter(prefecture__icontains=keyword))]
    else:
        post_list = []
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_cit_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'name': str(post[0])} for post in list(
            BlogPost.objects.distinct().values_list('city').filter(city__icontains=keyword))]
    else:
        post_list = []
    return JsonResponse({'object_list': post_list})

def search_post(request):
    if request.method == "GET":
        keyword_form = SearchPostKeywordForm(request.GET)
        option_form = SearchPostOptionForm(request.GET)
        latest_posts = get_public_post_list(BlogPost.objects.all().order_by('-created_at')[:20])
        if keyword_form.is_valid() and option_form.is_valid():
            search_results = get_public_post_list(search(request))
            if len(search_results) > 0:
                messages.add_message(request, messages.SUCCESS, _("Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _("Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'post_list': search_results, 'keyword_form': keyword_form, 'option_form': option_form, 'is_searched': True})
            else:
                messages.add_message(request, messages.SUCCESS, _("No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _("You might want to try changing to a keyword with a larger population."))
                return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'option_form': option_form, 'is_searched': True})
    keyword_form = SearchPostKeywordForm()
    option_form = SearchPostOptionForm()
    return render(request, 'search/search_blog_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'option_form': option_form, 'is_searched': False})

def search(request):
    query_keyword_string, sort_method = parse_search_request(request)
    if not query_keyword_string:
        return []
    else:
        query_words = query_keyword_string.split(' ')
        search_results = []
        if query_words is None:
            query_words = query
        for word in query_words:
            records_per_word = []
            records_per_word += BlogPost.objects.filter(title__icontains=word)
            for record in records_per_word:
                if record not in search_results:
                    search_results.append(record)
            search_results = sort_post_records_by(search_results, sort_method)
        return search_results

def search_post_ajax(request):
    if request.method == "GET":
        q = request.GET.get('q')
        search_results = get_public_post_list(search_ajax(q))
        if len(search_results) > 5:
            search_results = search_results[:5]
        minimal_search_results = [{'title': result.title} for result in search_results]
        if len(minimal_search_results) > 0:
            return JsonResponse(minimal_search_results, safe=False)
        else:
            return JsonResponse({'status':'false'}, status=500)

def search_ajax(q):
        query_words = q.split(' ')
        search_results = []
        if query_words is None:
            query_words = query
        for word in query_words:
            records_per_word = []
            records_per_word += Post.objects.filter(title__icontains=word)
            for record in records_per_word:
                if record not in search_results:
                    search_results.append(record)
        return search_results

def parse_search_request(request):
    query_keyword_string = request.GET.get("q")
    sort_method = request.GET.get("sort_method")
    return (query_keyword_string, sort_method)

def sort_post_records_by(post_records, sort_method):
    if sort_method == 'sort_new':
        return sorted(post_records, key=lambda instance: instance.created_at, reverse=True)
    elif sort_method == 'sort_old':
        return sorted(post_records, key=lambda instance: instance.created_at)
    return post_records

def search_tag(request):
    if request.method == "GET":
        q = request.GET.get('q_tag')
        tag_form = SearchPostTagForm(request.GET)
        if q:
          try:
            tag = BlogTag.objects.get(name=q)
          except:
            tag = False
            latest_posts = get_public_post_list(BlogPost.objects.all().order_by('-created_at')[:20])
          if tag:
            latest_posts = get_public_post_list(BlogPost.objects.all().order_by('-created_at').filter(tags=tag)[:10])
        else:
            latest_posts = get_public_post_list(BlogPost.objects.all().order_by('-created_at')[:20])
        tags_all = BlogTag.objects.all()
        if tag_form.is_valid():
            try:
                tag = BlogTag.objects.get(name=q)
                post_list = get_public_post_list(BlogPost.objects.filter(tags=tag))
                messages.add_message(request, messages.SUCCESS, "Your post has been found!")
                messages.add_message(request, messages.SUCCESS, "Up to 20 found posts will be displayed on one page")
                return render(request, 'search/search_blog_by_tag.html', {'latest_post_list': latest_posts, 'post_list': post_list, 'tag_form': tag_form, 'tags': tags_all, 'is_searched': True})
            except:
                messages.add_message(request, messages.SUCCESS, "No relevant posts found.")
                messages.add_message(request, messages.SUCCESS, "Discover the tags that interest you in our tag list!")
                messages.add_message(request, messages.SUCCESS, "However, there are cases where only tags are present")
                return render(request, 'search/search_blog_by_tag.html', {'latest_post_list': latest_posts, 'tag_form': tag_form, 'tags': tags_all, 'is_searched': True})
    tag_form = SearchPostTagForm()
    return render(request, 'search/search_blog_by_tag.html', {'latest_post_list': latest_posts, 'tag_form': tag_form, 'tags': tags_all, 'is_searched': False})
