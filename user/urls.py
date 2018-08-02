from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login,name='login'),
    path('login_for_modal/',views.login_for_modal,name='login_for_modal'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
]