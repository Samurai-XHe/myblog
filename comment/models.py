from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.conf import settings

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')  # 评论对象

    user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE) # 评论人
    comment_time = models.DateTimeField(auto_now_add=True) # 评论时间
    text = models.TextField() # 评论内容

    root = models.ForeignKey('self',related_name='root_comment',on_delete=models.CASCADE,null=True)     # 顶级评论
    parent = models.ForeignKey('self',related_name='parent_comment',on_delete=models.CASCADE,null=True) # 上级评论
    reply_to = models.ForeignKey(User,related_name='replies',on_delete=models.CASCADE,null=True)        # 上级评论的作者

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
