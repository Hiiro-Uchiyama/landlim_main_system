from django import template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from django.urls import reverse
import re

register = template.Library()

@register.inclusion_tag('post/_pagenated_post_list.html')
def show_pagenated_post_list(request, post_list):
    paginator = Paginator(post_list, settings.POST_NUM_PER_PAGE)
    page = request.GET.get('page')
    paginated_post_list = paginator.get_page(page)
    url_with_params = re.sub('(\?|&)page=\d+','',request.get_full_path())
    print(url_with_params)
    if '?' in url_with_params:
        url_with_params += '&'
    else:
        url_with_params += '?'
    return {'post_list': paginated_post_list, 'url_with_params': url_with_params}