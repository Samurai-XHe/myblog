from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'})
    )
    def clean(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('用户名或密码不能含有空格')
        password = self.cleaned_data['password']
        if ' ' in password:
            raise forms.ValidationError('用户名或密码不能含有空格')
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
