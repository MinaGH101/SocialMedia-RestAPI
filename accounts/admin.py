from django.contrib import admin
from .models import Post, Relation, Comments, Vote, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'slug', 'updated')
    search_fields = ('body',)
    list_filter = ('created',)
    prepopulated_fields = {'slug':('body',)}
    raw_id_fields = ('user',)
    
    
@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):   
    list_display = ('id','user', 'post', 'is_reply', 'created')
    raw_id_fields = ('user',)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    
class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    
admin.site.register(Relation)
admin.site.register(Profile)
admin.site.register(Vote)
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
