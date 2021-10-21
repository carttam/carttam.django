from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *
# Register your models here.
@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    #list_display = ['id','title']
    pass
@admin.register(Answer)
class AdminAnwer(admin.ModelAdmin):
    #list_display = ['id','user', 'answer']
    pass
@admin.register(UserImage)
class AdminUserImage(admin.ModelAdmin):
    #list_display = ['id','user', 'answer']
    pass