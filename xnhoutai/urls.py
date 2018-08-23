from django.urls import path
from django.views import generic

app_name = 'xnhoutai'
urlpatterns = [
    path('',generic.TemplateView.as_view(template_name='xnhoutai/home.html'),name='home'),
]