from django.shortcuts import render
from django.views.generic import TemplateView
from blog.utils import get_today_hot_blog,get_week_hot_blog,get_month_hot_blog


def index(request):
    context = {}
    context['today_hot_blogs'] = get_today_hot_blog()
    context['week_hot_blogs'] = get_week_hot_blog()
    context['month_hot_blogs'] = get_month_hot_blog()
    return render(request,'index.html',context)
