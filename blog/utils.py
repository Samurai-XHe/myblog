import datetime
from django.utils import timezone
from django.db.models import Sum
from .models import Blog


def get_week_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
        .filter(read_detail__date__lte=today, read_detail__date__gt=date)\
        .annotate(week_hot_sum=Sum('read_detail__one_day_read_count'))\
        .order_by('-week_hot_sum')
    return blogs[:7]


def get_month_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    blogs = Blog.objects\
        .filter(read_detail__date__lte=today, read_detail__date__gt=date)\
        .annotate(month_hot_sum=Sum('read_detail__one_day_read_count'))\
        .order_by('-month_hot_sum')
    return blogs[:7]