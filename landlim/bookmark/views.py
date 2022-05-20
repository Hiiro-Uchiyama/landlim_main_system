import bookmark
from .models import Bookmark
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from post.models import Post
from post.views import post_details
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

@login_required
def bookmark(request):
    bookmark = Bookmark.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'bookmark/bookmark.html', {'bookmark': bookmark})

@login_required
def bookmark_map(request):
    bookmark = Bookmark.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'bookmark/bookmark_map.html', {'bookmark': bookmark})

@ login_required
def bookmark_ajax(request):
    if request.POST.get('action') == 'post':
        result = ''
        pk = int(request.POST.get('postid'))
        post = get_object_or_404(Post, pk=pk)
        bookmarked = Bookmark.objects.filter(user=request.user, bookmark=post)
        if bookmarked:
            bookmark = Bookmark.objects.filter(user=request.user, bookmark=post)
            bookmark.delete()
            post.decrement_bookmark_count()
            result = post.bookmark_count
            return JsonResponse({'result': result})
        else:
            bookmark = Bookmark.objects.create(user=request.user)
            bookmark = bookmark.bookmark.add(post)
            post.increment_bookmark_count()
            result = post.bookmark_count
            return JsonResponse({'result': result})