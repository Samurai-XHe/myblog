from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,RegisterForm,ChangeNickNameForm
from .models import Profile

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('index')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request,'user/login.html',context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def user_info(request):
    return render(request,'user/user_info.html')

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from',reverse('index')))

def register(request):
    referer = request.GET.get('from')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']

            # 写入数据库
            new_user = User.objects.create_user(username=username,password=password,email=email)
            # 顺便登录
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(referer,'/')
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request,'user/register.html',context)

def change_nickname(request):
    redirect_to = request.GET.get('from',reverse('index'))
    if request.method == 'POST':
        form = ChangeNickNameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNickNameForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back'] = redirect_to
    return render(request,'form.html',context)