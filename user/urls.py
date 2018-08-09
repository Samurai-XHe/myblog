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
    path('bind_email/',views.bind_email,name='bind_email'),
    path('send_verification_code/',views.send_verification_code,name='send_verification_code'),
    path('change_password/',views.change_password,name='change_password'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('send_verification_code_forget/',views.send_verification_code_forget,name='send_verification_code_forget'),
    path('change_forget_password/',views.change_forget_password,name='change_forget_password'),
    path('register_code/',views.register_code,name='register_code'),
]