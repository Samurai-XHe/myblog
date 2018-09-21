from blog.utils import get_week_hot_blog,get_month_hot_blog

def week_hot_blogs(request):
    return {'week_hot_blogs':get_week_hot_blog()}

def month_hot_blogs(request):
    return {'month_hot_blogs':get_month_hot_blog()}