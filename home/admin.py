from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


# @admin.register(User)
# class PostAdmin(admin.ModelAdmin):      
#     list_display = ('id','username')

    
admin.site.register(Question)
admin.site.register(Answer)