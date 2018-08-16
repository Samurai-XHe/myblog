from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount,LikeRecord
register = template.Library()

@register.simple_tag
def get_likes_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    likes_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
    return likes_count.liked_num

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model

@register.simple_tag(takes_context=True)   # takes_context=True 能使用模板内的所有context内的属性
def get_like_status(context,obj):  # 当使用takes_context=True时函数的第一个参数必须是context
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return 'btn btn-default btn-'
    if LikeRecord.objects.filter(content_type=content_type,object_id=obj.pk,user=user).exists():
        return 'btn btn-danger btn-'
    else:
        return 'btn btn-default btn-'