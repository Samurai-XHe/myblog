from django.urls import path
from django.views import generic

app_name = 'xnhoutai'
urlpatterns = [
    path('',generic.TemplateView.as_view(template_name='xnhoutai/home.html'),name='home'),
    path('user_manage/',generic.TemplateView.as_view(template_name='xnhoutai/user_manage.html'),name='user_manage'),
    path('user_serch/',generic.TemplateView.as_view(template_name='xnhoutai/user_serch.html'),name='user_serch'),
]