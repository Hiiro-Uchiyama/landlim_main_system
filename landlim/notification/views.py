from django.dispatch import receiver
from django.shortcuts import render
from .models import Notion

## It is considered a good idea to pull information from other models.
def notion_list(request):
    try:
        notion = Notion.objects.filter(receiver=request.user)
        return render(request, 'notion/notion.html', {'notion':notion})
    except Notion.DoesNotExist:
        return render(request, 'notion/notion.html')