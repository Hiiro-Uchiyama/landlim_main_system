from __future__ import unicode_literals
import re
from django.contrib import messages
from django.db.models.fields.files import ImageField
from .models import Post, Comment, PostImage, PostQuerySet, UserChoiceEmotionForPost
from bookmark.models import Bookmark
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostAddForm, PostImageForm, CommentAddForm, SaveLocationAddForm, VideoAddForm
from django.db.models import Q
from django.views import generic
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from post.utils import get_public_post_list, fetch_latest_sold_timeline
from PIL import Image
from django.core.files.storage import FileSystemStorage
import os
import glob
import reverse_geocoder
import random, string
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core import serializers
import json
from django.core.mail import send_mail
from geopy.distance import great_circle
from taggit.models import Tag
from pyokaka import okaka

def get_post_by_pk(request, pk):
    return get_object_or_404(Post, pk=pk)

def get_post_by_pk_for_chat(request, post_pk, wanting_user_pk):
    return get_object_or_404(Post, pk=post_pk)

def get_post_by_post_pk(request, post_pk):
    return get_object_or_404(Post, pk=post_pk)

def post_list(request):
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post/post_list.html', {'post': post})

def is_totally_valid(post_form, post_image_forms):
    if not post_form.is_valid():
        return False
    else:
        for post_image_form in post_image_forms:
            if not post_image_form.is_valid():
                return False
    return True

def def_color(emotion):
    if emotion == '喜び':
        return '#DD6882'
    elif emotion == '信頼':
        return '#68A90D'
    elif emotion == '恐れ':
        return '#1A0D0D'
    elif emotion == '驚き':
        return '#FFFCDB'
    elif emotion == '悲しみ':
        return '#274E8F'
    elif emotion == '嫌悪':
        return  '#341A0D'
    elif emotion == '怒り':
        return '#D00D0D'
    elif emotion == '期待':
        return '#FFDD22'
    elif emotion == '平穏':
        return '#F7EAEA'
    elif emotion == '容認':
        return '#9CD05B'
    elif emotion == '不安':
        return '#8F9CA9'
    elif emotion == '放心':
        return '#759CD0'
    elif emotion == '哀愁':
        return '#8F271A'
    elif emotion == 'うんざり':
        return '#9C8F8F'
    elif emotion == '苛立ち':
        return '#8F271A'
    elif emotion == '関心':
        return '#D05B0D'
    else:
        return '#fff'

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

@login_required
def add_post(request):
    if request.method == "POST":
        post_image_forms = []
        for i, _file in enumerate(request.FILES.getlist('image')):
            post_image_forms.append(PostImageForm(i, request.POST, {'image':_file}))
        post_form = PostAddForm(request.POST, request.FILES)
        if is_totally_valid(post_form, post_image_forms):
            pinX = request.POST.get("pin_x")
            pinY = request.POST.get("pin_y")
            LatitudeLongitude = (pinX, pinY),
            Areascode = reverse_geocoder.search(LatitudeLongitude)
            CityCode = Areascode[0]['name']
            PrefectureCode = Areascode[0]['admin1']
            Areascode = Areascode[0]['cc']
            emotional = request.POST['emotion']
            color = def_color(emotional)
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            post_form.save_m2m()
            for post_image_form in post_image_forms:
                post_image = post_image_form.save(commit=False)
                post_image.post = post
                post_image.save()
                post.postimage_set.add(post_image)
            post.country = (okaka.convert(Areascode))
            post.prefecture = (okaka.convert(PrefectureCode))
            post.city = (okaka.convert(CityCode))
            post.emotion = emotional
            post.color = color
            post.save()
            messages.add_message(request, messages.SUCCESS, _("Successfully submitted to LandLim"))
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, _("It did not post properly"))
            messages.add_message(request, messages.ERROR, _("Please check your post again"))
            messages.add_message(request, messages.ERROR, _("Is there a problem with the size of the video?"))
    else:
        post_form = PostAddForm()
    post_image_forms = [PostImageForm(_i) for _i in range(3)]
    return render(request, 'post/add_post.html', {'post_form': post_form, 'post_image_forms': post_image_forms})

## It would be a good idea to set up access rights on the back end.
@login_required
def save_your_location(request):
    if request.method == "POST":
        post_form = SaveLocationAddForm(request.POST, request.FILES)
        if post_form.is_valid():
            pinX = request.POST.get("pin_x")
            pinY = request.POST.get("pin_y")
            provisional = request.POST.get("provisional")
            LatitudeLongitude = (pinX, pinY),
            Areascode = reverse_geocoder.search(LatitudeLongitude)
            CityCode = Areascode[0]['city']
            PrefectureCode = Areascode[0]['admin1']
            Areascode = Areascode[0]['cc']
            emotional = request.POST['emotion']
            color = def_color(emotional)
            post = post_form.save(commit=False)
            post.user = request.user
            post.provisional = provisional
            post.country = (okaka.convert(Areascode))
            post.prefecture = (okaka.convert(PrefectureCode))
            post.city = (okaka.convert(CityCode))
            post.emotion = emotional
            post.color = color
            post.save()
            messages.add_message(request, messages.SUCCESS, _("Successfully submitted to LandLim"))
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, _("It did not post properly"))
            messages.add_message(request, messages.ERROR, _("Please check your post again"))
            messages.add_message(request, messages.ERROR, _("Is there a problem with the size of the video?"))
    else:
        post_form = SaveLocationAddForm()
    return render(request, 'post/save_your_location.html', {'post_form': post_form})

def make_post_image_forms(request):
    post_image_forms = []
    for i, _file in enumerate(request.FILES.getlist('image')):
        post_image_forms.append(PostImageForm(i, request.POST, {'image':_file}))
    return post_image_forms

def get_posted_post_images(request):
    posted_images = request.FILES.getlist('image')
    return posted_images

@login_required
def update_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post_user_id = post.user.id
    if post_user_id != request.user.id:
        messages.add_message(request, messages.ERROR, _("That post may not be yours"))
        return HttpResponse(_("You don't seem to have permission to edit your post"))
    else:
        if request.method == "POST":
            post_form = PostAddForm(request.POST, instance=post)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                messages.add_message(request, messages.SUCCESS, _("Your post has been changed"))
                return redirect('post:post_details', pk=post.pk)
    post_form = PostAddForm(request.POST, instance=post)
    messages.add_message(request, messages.ERROR, _("I was not able to edit my post"))
    messages.add_message(request, messages.ERROR, _("Please make sure you have filled in all the information"))
    return render(request, 'post/update_post.html', {'post_form': post_form, 'post': post})

@login_required
def this_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_user_id = post.user.id
    if post_user_id != request.user.id:
        messages.add_message(request, messages.ERROR, _("That post may not be yours"))
        return HttpResponse(_("You don't seem to have permission to edit your post"))
    else:
        if request.method == "POST":
            post_form = PostAddForm(request.POST, instance=post)
            post_image_forms = make_post_image_forms(request)
            if is_totally_valid(post_form, post_image_forms):
                post = post_form.save(commit=False)
                post.seller = request.user
                post.save()
                changed_image_flags = [request.POST['image_'+str(i)+'_exists'] for i in range(3)]
                changed_flag_1_length = len([_ for _ in changed_image_flags if _ == '1'])
                before_post_images = [bpi for bpi in post.postimage_set.all()]
                posted_images = get_posted_post_images(request)
                posted_image_index = 0
                for image_form_index, flag in enumerate(changed_image_flags):
                    if flag == '1':
                        if posted_image_index < len(posted_images):
                            if image_form_index < len(before_post_images):
                                post_image = before_post_images[image_form_index]
                                post_image.image = post_image_forms[posted_image_index].save(commit=False).image
                                post_image.post = post
                                post_image.update()
                                posted_image_index += 1
                            else:
                                post_image = post_image_forms[posted_image_index].save(commit=False)
                                post_image.post = post
                                post_image.save()
                                post.postimage_set.add(post_image)
                                post.save()
                                posted_image_index += 1
                    elif flag == '2':
                        before_post_image = before_post_images[image_form_index]
                        before_post_image.delete()
                messages.add_message(request, messages.SUCCESS, _("Your post has been changed"))
                return redirect('post:post_details', pk=post.pk)
        post_form = PostAddForm(instance=post)
        post_image_forms = []
        post_images = post.postimage_set.all()
        post_image_thumbnail_urls = [post_image.thumbnail_url for post_image in post_images]
        for _i in range(3):
            if _i < len(post_images):
                post_image_forms.append(PostImageForm(_i, instance=post_images[_i]))
            else:
                post_image_forms.append(PostImageForm(_i))
        return render(request, 'post/this_post.html', {'post_form': post_form, 'post_image_forms': post_image_forms, 'post':post, 'post_image_thumbnail_urls': post_image_thumbnail_urls, 'placeholder_image_number_list': range(len(post_image_thumbnail_urls), 3)})

def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.filter(post=post).order_by('-like_count')
    bookmark = Bookmark.objects.filter(post=post)
    bookmarked = len(bookmark)
    if request.user.pk:
        post.increment_watched_count()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentAddForm(request.POST or None)
            if form.is_valid():
                comment_text = request.POST.get('comment_text')
                user = request.user
                comment = Comment.objects.create(
                    post=post, user=user, comment_text=comment_text)
                comment.save()
                post.increment_comment_count()
                comment = Comment.objects.filter(post=post).order_by('-like_count')
                messages.add_message(request, messages.SUCCESS, _("Your comment has been posted successfully!"))
    form = CommentAddForm()
    if post.postimage_set.first() == True:
        ogp_image_url = post.postimage_set.first().thumbnail_url
        return render(request, 'post/post_details.html', {'post': post, 'comment': comment, 'form': form, 'ogp_image_url': ogp_image_url, 'bookmarked': bookmarked})
    return render(request, 'post/post_details.html', {'post': post, 'comment': comment, 'form': form, 'bookmarked': bookmarked})

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('post:post_detail', post_id=comment.post.id)

@login_required
def comment_pagination(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post_user_id = post.user.id
    if post_user_id != request.user.id:
        messages.add_message(request, messages.ERROR, _("That post may not be yours"))
        return HttpResponse(_("You don't seem to have permission to delete posts"))
    else:
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()
        messages.add_message(request, messages.SUCCESS, _("LandLim has deleted the post."))

def is_valid_q(q):
    return q != '' and q is not None

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('post:post_detail', post_id=comment.post.id)

@login_required
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
    model = Post
    paginate_by = 10
    date_field = 'created_at'
    template_name = 'post/post_list.html'
    allow_empty = True
    make_object_list = True

class PostArchiveIndex(PostArchiveMixin, generic.ArchiveIndexView):
    pass

class PostYearArchiveIndex(PostArchiveMixin, generic.YearArchiveView):
    pass

class PostMonthArchiveIndex(PostArchiveMixin, generic.MonthArchiveView):
    month_format = '%m'

class PostDetail(generic.DetailView):
    model = Post

class PostList(generic.ListView):
    model = Post

class PostDetail(generic.DetailView):
    model = Post

@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('postid'))
        post = get_object_or_404(Post, pk=pk)
        if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.like.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        return JsonResponse({'result': result})

@ login_required
def dislike(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('postid'))
        post = get_object_or_404(Post, pk=pk)
        if post.dislike.filter(id=request.user.id).exists():
            post.dislike.remove(request.user)
            post.dislike_count -= 1
            result = post.dislike_count
            post.save()
        else:
            post.dislike.add(request.user)
            post.dislike_count += 1
            result = post.dislike_count
            post.save()
        return JsonResponse({'result': result})

@ login_required
def comment_like(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('commentid'))
        comment = get_object_or_404(Comment, pk=pk)
        if comment.like.filter(id=request.user.id).exists():
            comment.like.remove(request.user)
            comment.like_count -= 1
            result = comment.like_count
            comment.save()
        else:
            comment.like.add(request.user)
            comment.like_count += 1
            result = comment.like_count
            comment.save()
        return JsonResponse({'result': result})

@ login_required
def discomment_like(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('commentid'))
        comment = get_object_or_404(Comment, pk=pk)
        if comment.dislike.filter(id=request.user.id).exists():
            comment.dislike.remove(request.user)
            comment.dislike_count -= 1
            result = comment.dislike_count
            comment.save()
        else:
            comment.dislike.add(request.user)
            comment.dislike_count += 1
            result = comment.dislike_count
            comment.save()
        return JsonResponse({'result': result})

@ login_required
def add_emotion_for_post(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('postid'))
        post = get_object_or_404(Post, pk=pk)
        def_emotion = request.POST.get('def_emotion')
        def_emotion_color = request.POST.get('def_emotion_color')
        emotion = UserChoiceEmotionForPost.objects.create(
            def_emotion=def_emotion,def_emotion_color=def_emotion_color,own=request.user,post=post)
        emotion.save()
        ## I'm not sure about the process below this.
        if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.like.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        return JsonResponse({'result': result})

@ login_required
def comment(request, pk):
    if request.POST.get('action') == 'post':
        post = get_object_or_404(Post, pk=pk)
        comment_text = request.POST.get('comment_text')
        user = request.user
        comment = Comment.objects.create(
                    post=post, user=user, comment_text=comment_text)
        comment.save()
        ## You will receive a message when your comment is posted.
        ## You will receive an email or a small direct message at this time.
        ## How do I send a direct message?
        subject = "投稿にコメントされました"
        message = "あなたの投稿にコメントが追加されました。ぜひ確認してみて下さい。LandLim"
        from_email = post.user.email
        recipient_list = [from_email]
        send_mail(subject, message, from_email, recipient_list)
        post.increment_comment_count()
        comment = Comment.objects.filter(post=post).order_by('-created_at')[:1]
        jsoncomment =  serializers.serialize("json", Comment.objects.filter(post=post).order_by('-created_at')[:1])
        for i in comment:
            user_name = i.user.username
            user_icon = i.user.icon_url
        listcomment = eval(jsoncomment)
        listcomment.append({'username': user_name})
        listcomment.append({'user_icon': user_icon})
        Json = json.dumps(listcomment, ensure_ascii=False)
        return JsonResponse({'result': Json})

## The most unlikely function to be used.
def liked_timeline(request):
    MAX_NUM_LATEST_POST = 1000
    if request.user.country:
        country = request.user.country
        hight_liked_list = get_public_post_list(Post.objects.filter(country=country).order_by('-like_count')[:MAX_NUM_LATEST_POST])
        return render(request, 'like/liked_timeline.html', {'hight_liked_list': hight_liked_list})
    else:
        hight_liked_list = get_public_post_list(Post.objects.all().order_by('-like_count')[:MAX_NUM_LATEST_POST])
        return render(request, 'like/liked_timeline.html', {'hight_liked_list': hight_liked_list})

## It would be nice to be able to change the display range by user request.
def nearby_post(request):
    post = fetch_latest_sold_timeline()
    post_list = {}
    if request.user.pin_x and request.user.pin_y:
        pin_x = request.user.pin_x
        pin_y = request.user.pin_y
        user_location_object = (pin_y, pin_x)
    else:
        raise Exception
    for posts in post:
        lat = posts.pin_y
        lon = posts.pin_x
        post_location_object = (lat, lon)
        dis = great_circle(user_location_object, post_location_object).km
        if dis < 10:
            post_list.add(posts)
    return render(request, 'nearby/nearby_post.html', {'post':post_list})

## It would be nice to have a tag search to add features such as related articles.
def tag_linked_post(request, tag_id):
    tag = Tag.object.get(id=tag_id)
    post_list = Post.objects.filter(tag=tag)
    post = Post.objects.all()
    post.tags.similar_objects()
    return render(request, 'tag/tag_linked_post', {'tag':tag, 'post_list':post_list, 'post':post})

def country_linked_post(request, country):
    post_list = Post.objects.filter(country=country)
    countries = Post.objects.distinct().values_list('country')
    return render(request, 'country/country_linked_post', {'post_list':post_list, 'countries':countries})

def prefecture_linked_post(request, prefecture):
    post_list = Post.objects.filter(prefecture=prefecture)
    prefectures = Post.objects.distinct().values_list('prefecture')
    return render(request, 'country/country_linked_post', {'post_list': post_list, 'prefectures': prefectures})

def city_linked_post(request, city):
    post_list = Post.objects.filter(city=city)
    cities = Post.objects.distinct().values_list('city')
    return render(request, 'city/city_linked_post', {'post_list': post_list, 'cities': cities})

## On functions related to emotions
def emotion_linked_post(request, emotion):
    post_list = Post.objects.filter(emotion=emotion)
    emotions = Post.objects.distinct().values_list('emotion')
    return render(request, 'emotion/emotion_linked_post', {'post_list': post_list, 'emotions': emotions})

## It would be good to include other information.
## I would like to visualize the results of the emotional submission.
## It would be nice if we could narrow it down by month or something.
def emotion_visualization(request):
    emotions = Post.objects.distinct().values_list('emotion')
    ## Wouldn't it be nice to handle errors?
    pleasure_num = Post.objects.filter(emotion='喜び').count()
    trust_num = Post.objects.filter(emotion='信頼').count()
    fear_num = Post.objects.filter(emotion='恐れ').count()
    surprise_num = Post.objects.filter(emotion='驚き').count()
    sadness_num = Post.objects.filter(emotion='悲しみ').count()
    repugnance_num = Post.objects.filter(emotion='嫌悪').count()
    anger_num = Post.objects.filter(emotion='怒り').count()
    expectation_num = Post.objects.filter(emotion='期待').count()
    peaceful_num = Post.objects.filter(emotion='平穏').count()
    approval_num = Post.objects.filter(emotion='容認').count()
    anxiety_num = Post.objects.filter(emotion='不安').count()
    absentmindedness_num = Post.objects.filter(emotion='放心').count()
    sorrow_num = Post.objects.filter(emotion='哀愁').count()
    boring_num = Post.objects.filter(emotion='うんざり').count()
    irritation_num = Post.objects.filter(emotion='苛立ち').count()
    interest_num = Post.objects.filter(emotion='関心').count()
    context = {
        'emotions': emotions,
        'pleasure_num': pleasure_num,
        'trust_num': trust_num,
        'fear_num': fear_num,
        'surprise_num': surprise_num,
        'sadness_num': sadness_num,
        'repugnance_num': repugnance_num,
        'anger_num': anger_num,
        'expectation_num': expectation_num,
        'peaceful_num': peaceful_num,
        'approval_num': approval_num,
        'anxiety_num': anxiety_num,
        'absentmindedness_num': absentmindedness_num,
        'sorrow_num': sorrow_num,
        'boring_num': boring_num,
        'irritation_num': irritation_num,
        'interest_num': interest_num,
    }
    return render(request, 'emotion/emotion_num.html', context)

## Save the postings tied to the country.
## Perform validation with string type
## Retrieving relevant posts
def liked_user_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked_list = post.like
    return render(request, 'post/liked_user_list.html', {'liked_list':liked_list})

## Bookmark Bookmarking people list later.
## I need to decide what to do about bookmarks and such.
def bookmarked_user_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark = Bookmark.objects.filter(post=post)
    bookmarked_list = bookmark.user
    return render(request, 'post/bookmarked_user_list.html', {'bookmarked_list': bookmarked_list})

## It would be better to set up functions related to status and permissions.
@ login_required
def post_video(request):
    video_add_form = VideoAddForm()
    return render(request, 'post/add_video.html', {})

def view_videos(request):
    return render(request, 'video/view_video.html', {})

def search_videos(request):
    return render(request, 'video/search_video.html', {})
