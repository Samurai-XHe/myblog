from django.db.models import Count
from .models import Blog, BlogType


def blog_types(request):
    # 获取博客分类
    blog_types = BlogType.objects.annotate(blog_count=Count('blog'))
    return {'blog_types':blog_types}


def blog_dates(request):
    # 获取日期归档以及对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="ASC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    return {'blog_dates':blog_dates_dict}