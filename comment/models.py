from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from concurrent.futures import ThreadPoolExecutor


def send(email_title, user_email, email, html_message):
    send_mail(
        email_title,
        '',
        user_email,
        [email],
        fail_silently=False,
        html_message=html_message
    )


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # 评论对象

    user = models.ForeignKey(User,related_name='comments', on_delete=models.CASCADE)  # 评论人
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    text = models.TextField()  # 评论内容

    root = models.ForeignKey('self', related_name='root_comment', on_delete=models.CASCADE, null=True)     # 顶级评论
    parent = models.ForeignKey('self', related_name='parent_comment', on_delete=models.CASCADE, null=True)  # 上级评论
    reply_to = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE, null=True)        # 上级评论的作者

    def __str__(self):
        return self.text

    def send_email(self):
        if self.parent is None:
            # 评论博客
            email_title = '有人评论您的博客'
            url = self.content_object.get_url()
            email = self.content_object.get_email()
        else:
            # 回复评论
            email_title = '有人回复您的评论'
            url = self.parent.content_object.get_url()
            email = self.reply_to.email

        if email != '':
            context = {}
            context['email_text'] = self.text + url
            content = render_to_string('comment/send_email.html', context)
            thread = ThreadPoolExecutor(2)
            thread.submit(send, (email_title), (settings.EMAIL_HOST_USER), (email), (content))
            thread.shutdown(wait=False)

    class Meta:
        ordering = ['comment_time']
