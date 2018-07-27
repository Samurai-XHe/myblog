from django import forms
from django.core.validators import RegexValidator
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,
        max_length=10,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}),
        error_messages={
            'min_length': '用户名少于3位',
            'max_length': '用户名超过10位'
        },
        validators=[RegexValidator('/^[0-9a-zA-Z]*$/g','必须是数字和英文组合')]
    )
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}),
        error_messages = {
            'min_length': '密码少于8位',
            'max_length': '密码超过20位'
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', ' ')
        if ' ' in username:
            raise forms.ValidationError('用户名不能含有空格')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', ' ')
        if ' ' in password:
            raise forms.ValidationError('密码不能含有空格')
        return password


    def clean(self):
        username = self.cleaned_data.get('username',' ')
        password = self.cleaned_data.get('password',' ')
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data



