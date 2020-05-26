from django.contrib import admin
from Insta.models import Post, CustomUser, Like, Comment, UserConnection

# Register your models here. choose which model to show in the admin page
admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(UserConnection)