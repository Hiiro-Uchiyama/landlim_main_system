from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

def post_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            myself = form.cleaned_data['myself']
            recipients = [settings.EMAIL_HOST_USER]
            if myself:
                recipients.append(email)
            try:
                send_mail(name, message, email, recipients)
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            messages.add_message(request, messages.SUCCESS, _("Your enquiry has been sent to LandLim"))
            return render(request, 'contact/post_success.html')
    else:
        form = ContactForm()
    return render(request, 'contact/post_contact.html', {'form': form})