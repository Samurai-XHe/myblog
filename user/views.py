import random,time,string
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail

from .forms import LoginForm,RegisterForm,ChangeNickNameForm,BindEmailForm
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

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back'] = redirect_to
    return render(request,'user/bind_email.html',context)

def send_verification_code(request):
    email = request.GET.get('email','None')
    data = {}
    if email == '':
        data['status'] = 'ERROR'
        data['code'] = '401'
        data['message'] = '邮箱不能为空'
    else:
        if User.objects.filter(email=email).exists():
            data['status'] = 'ERROR'
            data['code'] = '402'
            data['message'] = '该邮箱已被使用，请换一个邮箱地址'
        else:
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            now = int(time.time())
            send_code_time = request.session.get('send_code_time',0)
            if now - send_code_time < 60:
                data['status'] = 'ERROR'
                data['code'] = '403'
                data['message'] = '您操作太频繁了'
            else:
                request.session[email] = code
                request.session['send_code_time'] = now
                send_mail(
                    '绑定邮箱',
                    '您的验证码：%s' % code,
                    '847834358@qq.com',
                    [email],
                    fail_silently=False,
                )
                data['status'] = 'SUCCESS'
    return JsonResponse(data)

