from django.urls import path,include
from . import views
from blog.views import blog_detail # 暂时
urlpatterns = [
    path('<int:blog_pk>',blog_detail,name='update_comment'),
]