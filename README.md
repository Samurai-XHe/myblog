本博客是跟随杨士航的教程写出的个人博客网站

博客主页 https://xhe.pythonanywhere.com/
###关于本博客
- - -
* 使用Django2.0 + BootStrap4
* 部署在pythonanywhere
* 图标库使用Font Awesome

###使用

---
1. 克隆本项目到本地
2. 在settings.py所在的目录新建base_settings.py
3. 在新建的base_settings.py内写入以下内容：

```
# 发送邮件设置
# https://docs.djangoproject.com/en/2.0/ref/settings/#email
# https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '你的邮箱地址'
EMAIL_HOST_PASSWORD = '你的邮箱授权码'  # 授权码
EMAIL_SUBJECT_PREFIX = '[xhe的博客] '
EMAIL_USE_SSL = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblog',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
4.启动项目即可
