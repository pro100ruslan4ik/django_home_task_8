from django.contrib import admin
from social_network import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('group', 'text', 'pub_date',)

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'post',)

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text_message', 'sender', 'receiver',)

@admin.register(models.UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at',)
