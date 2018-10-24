from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic import DetailView
from .models import Blog,BlogType
from read_statistics.utils import add_once_read


def base_data(request, blogs):
    try:
        page = int(request.GET.get('page', 1))
    except TypeError as e:
        page = 1
    # 分页器
    paginator = Paginator(blogs, settings.CONTENT_OF_EACH_PAGE)
    if page > paginator.num_pages or page < 1:
        page = 1
    page_of_blogs = paginator.get_page(page)
    # 获取页码范围
    page_range = [x for x in range(page - 2, page + 3) if x in paginator.page_range]
    # 加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和末页
    if page_range[0] == '...':
        page_range.insert(0, 1)
    if page_range[-1] == '...':
        page_range.append(paginator.num_pages)

    all_blogs = Blog.objects.all().count()
    context = {}
    context['all_blogs_count'] = all_blogs
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    return context


def blog_list(request):
    blogs = Blog.objects.all()
    context = base_data(request, blogs)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    blogs_list = Blog.objects.filter(blog_type=blog_type_pk)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context = base_data(request, blogs_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year,month):
    blogs_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = base_data(request, blogs_list)
    all_blogs = Blog.objects.filter(created_time__year=year, created_time__month=month).count()
    context['date_blog_count'] = all_blogs
    context['blogs_date'] = "%s年%s月" %(year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, pk):
    blog = get_object_or_404(Blog,pk=pk)
    read_session_key = add_once_read(request, blog)
    context = {}
    context['previous_page'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['next_page'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['blog'] = blog
    request.session[read_session_key] = 'true'   # 添加阅读session
    return render(request,'blog/blog_detail.html', context) # 响应


class blog_detail_0(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self):
        obj = super(blog_detail, self).get_object()
        read_session_key = add_once_read(self.request, obj)
        self.request.session[read_session_key] = 'true'  # 添加阅读session
        return obj

    def get_context_data(self, **kwargs):
        context = super(blog_detail, self).get_context_data()
        context['previous_page'] = Blog.objects.filter(created_time__lt=context['blog'].created_time).first()
        context['next_page'] = Blog.objects.filter(created_time__gt=context['blog'].created_time).last()
        return context
