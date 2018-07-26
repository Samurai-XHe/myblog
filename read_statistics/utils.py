import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog
from .models import ReadCount,OneDayReadCount


def add_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model,obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数+1
        readcount,xx = ReadCount.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readcount.read_count += 1
        readcount.save()

        #当天阅读数+1
        date = timezone.now().date()
        onedayreadcount,xx = OneDayReadCount.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        onedayreadcount.one_day_read_count += 1
        onedayreadcount.save()
    return key

def get_today_hot_blog():
    today = timezone.now().date()
    blogs = Blog.objects.filter(read_detail__date=today)
    return blogs[:7]

def get_week_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
        .filter(read_detail__date__lte=today,read_detail__date__gt=date)\
        .annotate(week_hot_sum=Sum('read_detail__one_day_read_count'))\
        .order_by('-week_hot_sum')
    return blogs[:7]

def get_month_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    blogs = Blog.objects\
        .filter(read_detail__date__lte=today,read_detail__date__gt=date)\
        .annotate(month_hot_sum=Sum('read_detail__one_day_read_count'))\
        .order_by('-month_hot_sum')
    return blogs[:7]
