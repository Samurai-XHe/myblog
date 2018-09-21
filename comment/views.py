from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('blog_list'))
    comment_form = CommentForm(request.POST,user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']

        #得到parent对象
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent if parent.root is None else parent.root
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #发送邮件通知
        comment.send_email()


        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime("%Y-%m-%d %H:%M")
        data['text'] = comment.text
        data['message'] = '评论成功'
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''

    else:
        data['status'] = 'ERROR'
        print(comment_form.errors.values())
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
