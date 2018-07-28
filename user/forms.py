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
            'max_length': '用户名超过10位',
            'required': '用户名不能为空!(这是forms字段验证)',
        },
        validators=[RegexValidator('^[a-zA-Z][a-zA-Z0-9_]{2,9}$','必须是数字和英文组合(这是validators)')]
    )
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}),
        error_messages = {
            'min_length': '密码少于8位',
            'max_length': '密码超过20位',
            'required': '密码不能为空!(这是forms字段验证)',
        },
        validators=[RegexValidator('^[a-zA-Z]\w{5,17}$', '必须是数字和英文组合(这是validators)')]
    )

    def clean(self):
        username = self.cleaned_data.get('username',' ')
        password = self.cleaned_data.get('password',' ')
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误(这是clean验证)')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'请输入3-10位的用户名',
            }
        ),
        error_messages={
            'required':'用户名不能为空',
            'max_length':'不能超过10位',
            'min_length':'不能少于3位',
        },
        validators=[RegexValidator('^[a-zA-Z][a-zA-Z0-9_]{2,9}$', '必须是数字和英文组合(这是validators)')]
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'请输入邮箱',
            }
        ),
        error_messages={
            'required': '邮箱不能为空',
        }
    )
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=23,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入8-23位的密码',
            }
        ),
        error_messages={
            'required': '密码不能为空',
            'max_length': '不能超过23位',
            'min_length': '不能少于8位',
        },
        validators=[RegexValidator('^[a-zA-Z]\w{5,17}$', '必须是数字和英文组合(这是validators)')]
    )
    password_again = forms.CharField(
        label='密码',
        min_length=8,
        max_length=23,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请再输一遍密码',
            }
        ),
        error_messages={
            'required': '密码不能为空',
            'max_length': '不能超过23位',
            'min_length': '不能少于8位',
        }
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已存在(这是clean_username验证)')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.Validationerror('该邮箱已被使用')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致(这是clean_password_again验证)')
        return password_again

