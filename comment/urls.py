from django.urls import path,include
from . import views
urlpatterns = [
    path('update_comment/',views.update_comment,name='update_comment'),
]