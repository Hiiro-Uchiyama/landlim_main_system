from django.shortcuts import render, get_object_or_404, redirect
from django.test import tag
from django.utils import timezone
from post.models import Post
from .forms import SearchPostKeywordForm, SearchPostOptionForm, SearchPostTagForm, SearchPostCouForm, SearchPostPreForm, SearchPostCitForm, SearchPostEmoForm, SearchPostRefineForm
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from post.utils import get_public_post_list
from django.views.generic.list import ListView
from taggit.models import Tag
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
from django.db.models import Q

## Complementary to the submission.
def api_posts_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'name': str(post[0])} for post in list(Post.objects.distinct().values_list('title').filter(title__icontains=keyword))]
    else:
        post_list = []
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_tags_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        tag_list = [{'name': str(tags[0])} for tags in list(Tag.objects.distinct().values_list('name').filter(name__icontains=keyword))]
    else:
        tag_list = []
    return JsonResponse({'object_list': tag_list})

## Complementary to the submission.
def api_cou_get(request):
    post_list = [{'name': str(post[0])} for post in list(Post.objects.distinct().values_list('country').order_by('country'))]
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_pre_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'name': str(post[0])} for post in list(Post.objects.distinct().values_list('prefecture').filter(prefecture__icontains=keyword))]
    else:
        post_list = []
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_cit_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'name': str(post[0])} for post in list(
            Post.objects.distinct().values_list('city').filter(city__icontains=keyword))]
    else:
        post_list = []
    return JsonResponse({'object_list': post_list})

## Complementary to the submission.
def api_emo_get(request):
    post_list = [{'name': str(post[0])} for post in list(Post.objects.distinct().values_list('emotion').order_by('emotion'))]
    return JsonResponse({'object_list': post_list})

def search_post(request):
    if request.method == "GET":
        keyword_form = SearchPostKeywordForm(request.GET)
        option_form = SearchPostOptionForm(request.GET)
        latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at')[:20])
        if keyword_form.is_valid() and option_form.is_valid():
            search_results = get_public_post_list(search(request))
            if len(search_results) > 0:
                messages.add_message(request, messages.SUCCESS, _("Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _("Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_by_title.html', {'latest_post_list': latest_posts, 'post_list': search_results, 'keyword_form': keyword_form, 'option_form': option_form, 'is_searched': True})
            else:
                messages.add_message(request, messages.SUCCESS, _("No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _("You might want to try changing to a keyword with a larger population."))
                return render(request, 'search/search_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'option_form': option_form, 'is_searched': True})
    keyword_form = SearchPostKeywordForm()
    option_form = SearchPostOptionForm()
    return render(request, 'search/search_by_title.html', {'latest_post_list': latest_posts, 'keyword_form': keyword_form, 'option_form': option_form, 'is_searched': False})

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
            records_per_word += Post.objects.filter(title__icontains=word)
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
        if q:
          try:
            tag = Tag.objects.get(name=q)
          except:
            tag = False
            latest_posts = get_public_post_list(
                Post.objects.all().order_by('-created_at')[:20])
          if tag:
            latest_posts = get_public_post_list(
                Post.objects.all().order_by('-created_at').filter(tags=tag)[:10])
        else:
            latest_posts = get_public_post_list(
                Post.objects.all().order_by('-created_at')[:20])
        tags_all = Tag.objects.all()
        if tag_form.is_valid():
            try:
                tag = Tag.objects.get(name=q)
                post_list = get_public_post_list(Post.objects.filter(tags=tag))
                messages.add_message(request, messages.SUCCESS, _(
                    "Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _(
                    "Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_by_tag.html', {'latest_post_list': latest_posts, 'post_list': post_list, 'tag_form': tag_form, 'tags': tags_all, 'is_searched': True})
            except:
                messages.add_message(request, messages.SUCCESS, _(
                    "No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _(
                    "Discover the tags that interest you in our tag list!"))
                messages.add_message(request, messages.SUCCESS, _(
                    "However, there are cases where only tags are present"))
                return render(request, 'search/search_by_tag.html', {'latest_post_list': latest_posts, 'tag_form': tag_form, 'tags': tags_all, 'is_searched': True})
    tag_form = SearchPostTagForm()
    return render(request, 'search/search_by_tag.html', {'latest_post_list': latest_posts, 'tag_form': tag_form, 'tags': tags_all, 'is_searched': False})

def search_area_cou(request):
    post = get_public_post_list(Post.objects.all().order_by('-created_at'))
    country = []
    for posts in post:
        if not posts.country in country:
            country.append(posts.country)
    if request.method == "GET":
        q_cou = request.GET.get('q_cou')
        if q_cou:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at').filter(prefecture=q_cou)[:10])
        else:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at')[:20])
        if cou_form.is_valid():
            post_list_cou = get_public_post_list(Post.objects.filter(country=q_cou))
            if len(post_list_cou) <= 0:
                messages.add_message(request, messages.SUCCESS, _("No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _("Discover the tags that interest you in our tag list!"))
                messages.add_message(request, messages.SUCCESS, _("However, there are cases where only tags are present"))
                return render(request, 'search/search_by_area_cou.html', {'latest_post_list': latest_posts, 'cou_form': cou_form, 'is_searched': True, 'country': country})
            else:
                messages.add_message(request, messages.SUCCESS, _("Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _("Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_by_area_cou.html', {'latest_post_list': latest_posts, 'post_list': post_list_cou, 'cou_form': cou_form, 'is_searched': True, 'country': country})
    cou_form = SearchPostCouForm()
    return render(request, 'search/search_by_area_cou.html', {'latest_post_list': latest_posts, 'cou_form': cou_form, 'is_searched': False, 'country': country})

def search_area_pre(request):
    post = get_public_post_list(Post.objects.all().order_by('-created_at'))
    prefecture = []
    for posts in post:
        if not posts.prefecture in prefecture:
            prefecture.append(posts.prefecture)
    if request.method == "GET":
        q_pre = request.GET.get('q_pre')
        if q_pre:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at').filter(prefecture=q_pre)[:10])
        else:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at')[:20])
        if pre_form.is_valid():
            post_list_cou = get_public_post_list(Post.objects.filter(country=q_pre))
            if len(post_list_cou) <= 0:
                messages.add_message(request, messages.SUCCESS, _("No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _("Discover the tags that interest you in our tag list!"))
                messages.add_message(request, messages.SUCCESS, _("However, there are cases where only tags are present"))
                return render(request, 'search/search_by_area_cou.html', {'latest_post_list': latest_posts, 'pre_form': pre_form, 'is_searched': True, 'prefecture': prefecture})
            else:
                messages.add_message(request, messages.SUCCESS, _("Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _("Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_by_area_cou.html', {'latest_post_list': latest_posts, 'post_list': post_list_cou, 'pre_form': pre_form, 'is_searched': True, 'prefecture': prefecture})
    pre_form = SearchPostPreForm()
    return render(request, 'search/search_by_area_pre.html', {'latest_post_list': latest_posts, 'pre_form': pre_form, 'is_searched': False, 'prefecture': prefecture})

def search_area_city(request):
    post = get_public_post_list(Post.objects.all().order_by('-created_at'))
    city = []
    for posts in post:
        if not posts.city in city:
            city.append(posts.city)
    if request.method == "GET":
        q_cit = request.GET.get('q_cit')
        if q_cit:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at').filter(city=q_cit)[:10])
        else:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at')[:20])
        if cit_form.is_valid():
            post_list_pre = get_public_post_list(Post.objects.filter(city=q_cit))
            if len(post_list_pre) <= 0:
                messages.add_message(request, messages.SUCCESS, _("No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _("Discover the tags that interest you in our tag list!"))
                messages.add_message(request, messages.SUCCESS, _("However, there are cases where only tags are present"))
                return render(request, 'search/search_by_area_city.html', {'latest_post_list': latest_posts, 'cit_form': cit_form, 'is_searched': True, 'city': city})
            else:
                messages.add_message(request, messages.SUCCESS, _("Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _("Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_by_area_city.html', {'latest_post_list': latest_posts, 'post_list': post_list_pre, 'cit_form': cit_form, 'is_searched': True, 'city': city})
    cit_form = SearchPostCitForm()
    return render(request, 'search/search_by_area_city.html', {'latest_post_list': latest_posts, 'pre_form': cit_form, 'is_searched': False, 'city': city})

def search_emotion(request):
    post = get_public_post_list(Post.objects.all().order_by('-created_at'))
    emotion = []
    for posts in post:
        if not posts.emotion in emotion:
            emotion.append(posts.emotion)
    if request.method == "GET":
        q_emo = request.GET.get('q_emo')
        if q_emo:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at').filter(emotion=q_emo)[:10])
        else:
            latest_posts = get_public_post_list(Post.objects.all().order_by('-created_at')[:20])
        if emo_form.is_valid():
            post_list_pre = get_public_post_list(Post.objects.filter(emotion=q_emo))
            if len(post_list_pre) <= 0:
                messages.add_message(request, messages.SUCCESS, _("No relevant posts found."))
                messages.add_message(request, messages.SUCCESS, _("Discover the tags that interest you in our tag list!"))
                messages.add_message(request, messages.SUCCESS, _("However, there are cases where only tags are present"))
                return render(request, 'search/search_by_emotion.html', {'latest_post_list': latest_posts, 'emo_form': emo_form, 'is_searched': True, 'emotion': emotion})
            else:
                messages.add_message(request, messages.SUCCESS, _("Your post has been found!"))
                messages.add_message(request, messages.SUCCESS, _("Up to 20 found posts will be displayed on one page"))
                return render(request, 'search/search_by_emotion.html', {'latest_post_list': latest_posts, 'post_list': post_list_pre, 'emo_form': emo_form, 'is_searched': True, 'emotion': emotion})
    emo_form = SearchPostEmoForm()
    return render(request, 'search/search_by_emotion.html', {'latest_post_list': latest_posts, 'emo_form': emo_form, 'is_searched': False, 'emotion': emotion})

## Let's review the search.
## Provide a search window with a suggestion function.
## def search_with_suggest(request)
## The name of the id may be different.
## It should have a related tag or something.
def search_refine(request):
    ## As for the emotional search, I think a selective system would be less confusing.
    refine_form = SearchPostRefineForm()
    refine_form.fields['q_cou'].choices += [
        ('', '選択しない'),
    ]
    refine_form.fields['q_emo'].choices += [
        ('', '選択しない'),
    ]
    if request.method == "GET":
        sort = request.GET.get('sort_method')
        q = request.GET.get('q', None)
        q_tag = request.GET.get('q_tag', None)
        q_cou = request.GET.get('q_cou', None)
        q_pre = request.GET.get('q_pre', None)
        q_cit = request.GET.get('q_cit', None)
        q_emo = request.GET.get('q_emo', None)
        if q or q_tag or q_cou or q_pre or q_cit or q_emo:
            if q_tag:
                try:
                    tag = Tag.objects.get(name=q_tag)
                except:
                    tag = None
                if sort == 'sort_new':
                    post_list = Post.objects.filter(
                        Q(title__contains=q),
                        Q(tags=tag),
                        Q(country__contains=q_cou),
                        Q(prefecture__contains=q_pre),
                        Q(city__contains=q_cit),
                        Q(emotion__contains=q_emo)).order_by('-id')
                else:
                    post_list = Post.objects.filter(
                        Q(title__contains=q),
                        Q(tags=tag),
                        Q(country__contains=q_cou),
                        Q(prefecture__contains=q_pre),
                        Q(city__contains=q_cit),
                        Q(emotion__contains=q_emo)).order_by('id')
            else:
                if sort == 'sort_new':
                    post_list = Post.objects.filter(
                        Q(title__contains=q),
                        Q(country__contains=q_cou),
                        Q(prefecture__contains=q_pre),
                        Q(city__contains=q_cit),
                        Q(emotion__contains=q_emo)).order_by('-id')
                else:
                    post_list = Post.objects.filter(
                        Q(title__contains=q),
                        Q(country__contains=q_cou),
                        Q(prefecture__contains=q_pre),
                        Q(city__contains=q_cit),
                        Q(emotion__contains=q_emo)).order_by('id')
            context = {
                'refine_form': refine_form,
                'post_list': post_list,
                'is_searched': True
            }
            print(post_list)
            return render(request, 'search/search_refine.html', context)
    context = {
        'refine_form': refine_form,
        'is_searched': None
    }
    return render(request, 'search/search_refine.html', context)
