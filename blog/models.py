from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import GetReadCount,OneDayReadCount
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class BlogType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Blog(models.Model,GetReadCount):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    read_detail = GenericRelation(OneDayReadCount,related_query_name='blog')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    cover = ProcessedImageField(verbose_name='封面',
                                 upload_to='cover_imgs/%y/%m/%d',
                                 processors=[ResizeToFill(150, 200)],
                                 default='cover_imgs/qq1.gif')

    def __str__(self):
        return '<Blog: %s>' % self.title

    def get_url(self):
        return reverse('blog_detail',kwargs={'pk':self.pk})

    def get_email(self):
        return self.author.email

    class Meta:
        ordering = ['-created_time']