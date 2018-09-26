import random,time, string,re
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import LoginForm, RegisterForm, ChangeNickNameForm, BindEmailForm
from .forms import ChangePassWordFormk, ForgetPasswordForm, ChangeForgetPasswordForm
from .models import Profile


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from', reverse('blog_list')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


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
    return render(request, 'user/user_info.html')


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('blog_list')))


def register(request):
    redirect_to = request.GET.get('from', reverse('blog_list'))
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']

            # 写入数据库
            new_user = User.objects.create_user(username=username, password=password, email=email)
            # 顺便登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(redirect_to, '/')
    else:
        register_form = RegisterForm()
    context = {}
    context['form'] = register_form
    context['page_title'] = '欢迎注册'
    context['form_title'] = '欢迎注册'
    context['submit_text'] = '注册'
    context['return_back'] = redirect_to
    return render(request, 'user/register.html', context)


def register_code(request):
    email = request.GET.get('email', 'None')
    data = {}
    if email == '':
        data['status'] = 'ERROR'
        data['code'] = '401'
        data['message'] = '邮箱不能为空'
    elif not re.search(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', email):
        data['status'] = 'ERROR'
        data['code'] = '400'
        data['message'] = '请输入正确的邮箱地址'
    else:
        if User.objects.filter(email=email).exists():
            data['status'] = 'ERROR'
            data['code'] = '402'
            data['message'] = '该邮箱已被使用，请换一个邮箱地址'
        else:
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            now = int(time.time())
            send_code_time = request.session.get('send_code_time', 0)
            if now - send_code_time < 30:
                data['status'] = 'ERROR'
                data['code'] = '403'
                data['message'] = '您操作太频繁了'
            else:
                request.session[email] = code
                request.session['send_code_time'] = now
                request.session['email'] = email
                send_mail(
                    '绑定邮箱',
                    '您的验证码：%s' % code,
                    '847834358@qq.com',
                    [email],
                    fail_silently=False,
                )
                data['status'] = 'SUCCESS'
                data['message'] = '发送成功'
    return JsonResponse(data)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('blog_list'))
    if request.method == 'POST':
        form = ChangeNickNameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
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
    return render(request,'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('blog_list'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session[email]
            del request.session['email']
            del request.session['send_code_time']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back'] = redirect_to
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', 'None')
    data = {}
    if email == '':
        data['status'] = 'ERROR'
        data['code'] = '401'
        data['message'] = '邮箱不能为空'
    elif not re.search(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', email):
        data['status'] = 'ERROR'
        data['code'] = '400'
        data['message'] = '请输入正确的邮箱地址'
    else:
        if User.objects.filter(email=email).exists():
            data['status'] = 'ERROR'
            data['code'] = '402'
            data['message'] = '该邮箱已被使用，请换一个邮箱地址'
        else:
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            now = int(time.time())
            send_code_time = request.session.get('send_code_time', 0)
            if now - send_code_time < 30:
                data['status'] = 'ERROR'
                data['code'] = '403'
                data['message'] = '您操作太频繁了'
            else:
                request.session[email] = code
                request.session['send_code_time'] = now
                request.session['email'] = email
                send_mail(
                    '绑定邮箱',
                    '您的验证码：%s' % code,
                    '847834358@qq.com',
                    [email],
                    fail_silently=False,
                )
                data['status'] = 'SUCCESS'
                data['message'] = '发送成功'
    return JsonResponse(data)


def change_password(request):
    redirect_to = request.GET.get('from', reverse('blog_list'))
    if request.method == 'POST':
        form = ChangePassWordFormk(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = form.cleaned_data['user']
            user.set_password(new_password)
            user.save()
            return redirect(reverse('user:login'))
    else:
        form = ChangePassWordFormk()
    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['return_back'] = redirect_to
    return render(request, 'user/change_password.html', context)


def forget_password(request):
    redirect_to = request.GET.get('from', reverse('blog_list'))
    context = {}
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            del request.session[email]
            del request.session['send_code_time']
            del request.session['username_or_email']
            return redirect(reverse('user:change_forget_password'))
    else:
        form = ForgetPasswordForm()
    context['form'] = form
    context['page_title'] = '忘记密码'
    context['form_title'] = '找回密码'
    context['submit_text'] = '提交'
    context['return_back'] = redirect_to
    return render(request, 'user/forget_password.html', context)


def send_verification_code_forget(request):
    username_or_email = request.GET.get('username_or_email', 'None')
    data = {}
    if username_or_email == '':
        data['status'] = 'ERROR'
        data['code'] = '401'
        data['message'] = '用户名或邮箱地址不能为空'
    elif not User.objects.filter(email=username_or_email).exists():
        if not User.objects.filter(username=username_or_email).exists():
            data['status'] = 'ERROR'
            data['code'] = '402'
            data['message'] = '您输入的用户名或邮箱地址不存在'
        else:
            email = User.objects.get(username=username_or_email).email
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            now = int(time.time())
            send_code_time = request.session.get('send_code_time', 0)
            if now - send_code_time < 30:
                data['status'] = 'ERROR'
                data['code'] = '403'
                data['message'] = '您操作太频繁了'
            else:
                request.session[email] = code
                request.session['send_code_time'] = now
                request.session['username_or_email'] = username_or_email
                request.session['email'] = email
                send_mail(
                    '找回密码',
                    '您的验证码：%s' % code,
                    '847834358@qq.com',
                    [email],
                    fail_silently=False,
                )
                data['status'] = 'SUCCESS'
                data['message'] = '发送成功'
    else:
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
            data['code'] = '403'
            data['message'] = '您操作太频繁了'
        else:
            request.session[username_or_email] = code
            request.session['send_code_time'] = now
            request.session['username_or_email'] = username_or_email
            request.session['email'] = username_or_email
            send_mail(
                '找回密码',
                '您的验证码：%s' % code,
                '847834358@qq.com',
                [username_or_email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
            data['message'] = '发送成功'
    return JsonResponse(data)


def change_forget_password(request):
    context ={}
    if request.session.get('email', '') != '':
        if request.method == 'POST':
            email = request.session['email']
            del request.session['email']
            form = ChangeForgetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return redirect(reverse('user:login'))
        else:
            form = ChangeForgetPasswordForm()
        context['form'] = form
        context['page_title'] = '重置密码'
        context['form_title'] = '重置密码'
        context['submit_text'] = '提交'
        return render(request, 'user/change_forget_password.html', context)
    else:
        return redirect(reverse('blog_list'))

