from django.contrib import admin
from django.urls import path,include
from blog import views

urlpatterns= [
    path('',views.blog_list,name='blog_list'),
    path('<int:blog_pk>/',views.blog_detail,name='blog_detail')
]