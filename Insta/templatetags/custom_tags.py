from django import template
from Insta.models import Like

register = template.Library()

@register.simple_tag
def has_user_liked_post(user, post):
    try:
        like = Like.objects.get(user=user, post=post)   # Like.objects: get all the objects in Like
        return 'fa-heart'
    except:
        return 'fa-heart-o'


@register.simple_tag
def is_following(from_user, to_user):
    return to_user.get_followers().filter(from_user=from_user).exists()