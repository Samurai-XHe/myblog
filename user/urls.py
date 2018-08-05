from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/',views.login,name='login'),
    path('login_for_modal/',views.login_for_modal,name='login_for_modal'),
    path('user_info/',views.user_info,name='user_info'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('change_nickname/',views.change_nickname,name='change_nickname'),
]