from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','nickname')
    search_fields = ('user__username','nickname')
    raw_id_fields = ('user',)
