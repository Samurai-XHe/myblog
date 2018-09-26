from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(
        widget=CKEditorWidget(config_name='comment_ckeditor'),
        error_messages={
            'required': '评论内容不能为空',
        }
    )
    reply_comment_id = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={'id':'reply_comment_id'}
        )
    )

    def __init__(self, *args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 评论对象验证
        content_type = self.cleaned_data.get('content_type', '')
        object_id = self.cleaned_data.get('object_id', '')
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data

    def clean_text(self):
        text = self.cleaned_data['text']   # 注意！ 表情等会被转译成img标签，因此统计字符数是个问题
        if len(text) <= 9:   # 因为text带有<p>标签，所以要比限制的字数多7个，这里是想限制不能少于3个字，所以是2+7=9
            raise forms.ValidationError('字数不能少于3个')
        elif len(text) > 5007:    # 因为text带有<p>标签，所以要比限制的字数多7个，这里是想限制不能超过100个字，所以是5000+7=5007
            raise forms.ValidationError('字数不能超过100个')
        return text

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data.get('reply_comment_id', '')
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错（id<0）')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id
