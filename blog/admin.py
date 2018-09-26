from django.contrib import admin
from .models import Blog,BlogType


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'created_time', 'last_updated_time')
    search_fields = ('title',) # 按字段名搜索
    list_filter = ('created_time',) # 按添加时间过滤,也可按布尔值或外键过滤，只要结果多于两个
    date_hierarchy = 'created_time'  # 也可以使用这个字段按时间分组，显示在表单上方，注意值是字符串不是元祖

    #以下是表单内的设置
    #fields = ('title','author') # 表单内只显示元祖内的字段，可以控制哪些字段不能修改
    raw_id_fields = ('author',) # 用来方便的查找外键字段
    #filter_horizontal = ('xxx',) # 用来方便的查找多对多字段，横向显示
    #filter_vertical = ('xxx',) # 用来方便的查找多对多字段，竖向显示