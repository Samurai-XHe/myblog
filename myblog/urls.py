"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views import generic
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',include('blog.urls')),
    path('user/',include('user.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('comment/',include('comment.urls')),
    path('likes/',include('likes.urls')),
    path('demo1/',generic.TemplateView.as_view(template_name='demo1.html'),name='demo1'),# 通用视图，Templateview连views函数都不用写,因为他只是单纯的返回一个静态网页，不需要函数对其处理
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
