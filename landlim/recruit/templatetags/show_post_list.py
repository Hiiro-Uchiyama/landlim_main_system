from django import template

register = template.Library()

@register.inclusion_tag('post/_post_list.html')
def show_post_list(post_list):
    return {'post_list': post_list}