from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Profile(models.Model):
    nickname = models.CharField('昵称', max_length=20)
    avatar = ProcessedImageField(
        verbose_name='头像',
        upload_to='avatar_imgs/%y/%m/%d',
        processors=[ResizeToFill(80, 80)],
        default='avatar_imgs/default.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname, self.user.username)


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username



def get_avatar_url(self):  # 利用这个方法可以在新用户没有头像的时候返回默认的头像
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.avatar
    else:
        return 'avatar_imgs/default.jpg'




User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username

