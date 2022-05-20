from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Report
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from post.models import Post
from accounts.views import others_page
from post.views import post_details
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

## To report a problem
## Some text It would be good to be able to input data, etc.
## A pop-up form would also be nice.
@login_required
def add_or_delete_report(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reported = Report.objects.filter(user=request.user, report=post)
    if reported:
        report = Report.objects.filter(user=request.user, report=post)
        report.delete()
        messages.add_message(request, messages.ERROR, _("The report has been withdrawn."))
        return post_details(request, pk)
    else:
        report = Report.objects.create(user=request.user)
        report = report.report.add(post)
        messages.add_message(request, messages.SUCCESS, _("The post Reported to LandLim!"))
        return post_details(request, pk)
