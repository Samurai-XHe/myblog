from django.contrib import admin
from .models import ReadCount, OneDayReadCount


@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    list_display = ('read_count', 'content_object')


@admin.register(OneDayReadCount)
class OneDayReadCountAdmin(admin.ModelAdmin):
    list_display = ('date', 'one_day_read_count', 'content_object')
