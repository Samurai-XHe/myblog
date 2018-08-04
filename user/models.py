from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    nickname = models.CharField('昵称',max_length=20)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname,self.user.username)
