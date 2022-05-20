from .models import AccessLevelChoice
from .models import Post

def get_public_post_list(post_list):
    return [post for post in post_list if post.access_level == AccessLevelChoice.public.name]

def fetch_latest_sold_timeline():
    post = get_public_post_list(Post.objects.all().order_by('-created_at'))
    post_dict_list = []
    for posts in post:
        if posts.postimage_set.first():
            post_dict_list.append(
                {
                    'user': posts.user,
                    'title': posts.title,
                    'text': posts.text,
                    'tag': posts.tags,
                    'image': posts.postimage_set.first().thumbnail_url,
                    'web_link': posts.web_link,
                    'twitter_link': posts.twitter_link,
                    'instagram_link': posts.instagram_link,
                    'pk': posts.pk,
                    'pin_x': posts.pin_x,
                    'pin_y': posts.pin_y,
                    'watched_count': posts.watched_count,
                    'like_count': posts.like_count,
                    'dislike_count': posts.dislike_count,
                    'bookmark_count': posts.bookmark_count,
                    'comment_count': posts.comment_count,
                    'created_at': posts.created_at,
                    'country': posts.country,
                    'prefecture': posts.prefecture,
                    'city': posts.city,
                    'emotion': posts.emotion,
                    'color': posts.color,
                    'like': posts.like,
                }
            )
        else:
            post_dict_list.append(
                {
                    'user': posts.user,
                    'title': posts.title,
                    'text': posts.text,
                    'tag': posts.tags,
                    'web_link': posts.web_link,
                    'twitter_link': posts.twitter_link,
                    'instagram_link': posts.instagram_link,
                    'pk': posts.pk,
                    'pin_x': posts.pin_x,
                    'pin_y': posts.pin_y,
                    'watched_count': posts.watched_count,
                    'like_count': posts.like_count,
                    'dislike_count': posts.dislike_count,
                    'bookmark_count': posts.bookmark_count,
                    'comment_count': posts.comment_count,
                    'created_at': posts.created_at,
                    'country': posts.country,
                    'prefecture': posts.prefecture,
                    'city': posts.city,
                    'emotion': posts.emotion,
                    'color': posts.color,
                    'like': posts.like,
                }
            )
    return post_dict_list
