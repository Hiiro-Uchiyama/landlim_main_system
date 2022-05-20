from django.contrib import admin
from message.models import Message
from .models import User, Entry

admin.site.register(Message)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Entry)
class Entry(admin.ModelAdmin):
    pass