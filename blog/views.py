from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog,BlogType

def base_data():
    pass

def blog_list(request):
    page = int(request.GET.get('page',1))
    blogs = Blog.objects.all()
    paginator = Paginator(blogs,settings.CONTENT_OF_EACH_PAGE)
    if page > paginator.num_pages or page < 1:
        page = 1
    page_of_blogs = paginator.get_page(page)
    # 获取页码范围
    page_range = [x for x in range(page - 2,page + 3) if x in paginator.page_range]
    # 加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和末页
    if page_range[0] == '...':
        page_range.insert(0,1)
    if page_range[-1] == '...':
        page_range.append(paginator.num_pages)
    context = {}
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    return render(request,'blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)

    context = {}
    context['previous_page'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['next_page'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['blog'] = blog
    return render(request, 'blog/blog_detail.html', context)