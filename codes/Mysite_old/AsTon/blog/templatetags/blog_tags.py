from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def get_recent_posts(num=2):
    return Post.objects.all().order_by('-created_time')[:num]