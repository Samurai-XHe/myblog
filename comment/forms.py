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
            'required': '评论内容不能为空,接口提交？',
        }
    )

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args,**kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 评论对象验证
        try:
            content_type = self.cleaned_data['content_type']
            object_id = self.cleaned_data['object_id']
        except Exception as e:
            raise forms.ValidationError('the object is not exists对象不存在')
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) <= 12:   #  因为text带有<p>标签，所以要比限制的字数多7个，这里是想限制不能少于6个字，所以是5+7=12
            raise forms.ValidationError('字数不能少于6个')
        elif len(text) > 107:    #  因为text带有<p>标签，所以要比限制的字数多7个，这里是想限制不能超过100个字，所以是100+7=107
            raise forms.ValidationError('字数不能超过10个')
        return text