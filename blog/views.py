from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog,BlogType


def blog_list(request):
    page = request.GET.get('page',1)
    blogs = Blog.objects.all()
    paginator = Paginator(blogs,settings.CONTENT_OF_EACH_PAGE)
    page_of_blogs = paginator.get_page(page)
    context = {}
    context['page_of_blogs'] = page_of_blogs
    return render(request,'blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    context = {}
    context['blog'] = blog
    return render(request, 'blog/blog_detail.html', context)