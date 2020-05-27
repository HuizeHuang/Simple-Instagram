from django import template
from Insta.models import Like
from django.urls import NoReverseMatch, reverse
import re

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


@register.simple_tag
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''