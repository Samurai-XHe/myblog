from django.urls import path
from blog.views import BlogListView, BlogWithTypeView, BlogWithDate, BlogDetailView


urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('type/<int:blog_type_pk>/', BlogWithTypeView.as_view(), name='blogs_with_type'),
    path('date/<int:year>/<int:month>/', BlogWithDate.as_view(), name='blogs_with_date')
]