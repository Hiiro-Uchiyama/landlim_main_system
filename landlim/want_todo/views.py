from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import WantToDo, WantToDoPoint
from .forms import WantToDoAddForm
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from post.models import Post
from accounts.models import User
from geopy.distance import great_circle

## Perform todo list display.
def want_todo_list(request):
    todo = WantToDo.objects.all().order_by('created_at')
    return render(request, 'want_todo/want_todo_list.html', {'todo': todo})

## You can see where you want to go.
def want_todo_map(request):
    todo = WantToDo.objects.all().order_by('created_at')
    return render(request, 'want_todo/want_todo_map.html', {'todo': todo})

## The list of things you want to do can be crossed off.
## It would be better not to let the map load again.
def delete_want_todo(request, pk):
    todo = get_object_or_404(WantToDo, pk=pk)
    todo_user_id = todo.user.id
    if todo_user_id != request.user.id:
        messages.add_message(request, messages.ERROR, _("That to-do list may not be yours!"))
        return HttpResponse(_("You don't seem to have permission to edit your to-do list"))
    else:
        todo = get_object_or_404(WantToDo, pk=pk)
        todo.delete()
        todo = WantToDo.objects.all().order_by('-created_at')
        messages.add_message(request, messages.SUCCESS, _("Things to do have been removed"))
        messages.add_message(request, messages.SUCCESS, _("Thank you for your time"))
    return render(request, 'want_todo/want_todo_list.html', {'todo': todo})

## Add a todo list.
def add_want_todo(request):
    if request.method == "POST":
        form = WantToDoAddForm(request.POST or None)
        if form.is_valid():
            title = request.POST.get('want_todo_title')
            text = request.POST.get('want_todo_text')
            pin_x= request.POST.get("pin_x")
            pin_y = request.POST.get("pin_y")
            todo = WantToDo.objects.create(
                user=request.user, title=title, text=text, pin_x=pin_x, pin_y=pin_y)
            todo.save()
            todo = WantToDo.objects.all().order_by('-created_at')
            messages.add_message(request, messages.SUCCESS, _("Added things to do"))
            ## Redirection would be better.
            return render(request, 'want_todo_list/want_todo_list.html', {'todo': todo})
        else:
            messages.add_message(request, messages.ERROR, _("I couldn't add anything to do"))
            messages.add_message(request, messages.ERROR, _("Character count may be a problem"))
            messages.add_message(request, messages.ERROR, _("Are you already logged in to LandLim?"))
    else:
        form = WantToDoAddForm()
    return render(request, 'want_todo/add_want_todo.html', {'form':form})

## Check if they have been there.
## It would be nice to be able to press a check button to obtain points.
def check_and_give_point(request, user_pk, post_pk, want_todo_pk):
    user = User.objects.filter(pk=user_pk)
    post = Post.objects.filter(pk=post_pk)
    want_todo = WantToDo.objects.filter(pk=want_todo_pk)
    if WantToDoPoint.objects.filter(user=user).exist():
        point = WantToDoPoint.objects.filter(user=user)
    else:
        point = WantToDoPoint.objects.create(user=user)
        point.save()
        point = WantToDoPoint.objects.filter(user=user)
    post_dis = (post.pin_y,post.pin_x)
    want_todo_dis = (want_todo.pin_y,want_todo.pin_x)
    dis = great_circle(post_dis, want_todo_dis).km
    if dis < 10:
        point.point += 10
        return True
    elif 10 <= dis < 50:
        point.point += 20
        return True
    elif 50 <= dis < 100:
        point.point += 50
        return True
    elif 100 <= dis < 500:
        point.point += 100
        return True
    elif 500 <= dis < 1000:
        point.point += 200
        return True
    elif 1000 <= dis:
        point.point += 500
        return True
    else:
        return None
