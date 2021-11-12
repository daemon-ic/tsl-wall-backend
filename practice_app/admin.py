from django.contrib import admin
from .models import Posts, Users

# NOT SURE WHAT THIS  IS YET


class PostsAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "postId", "username", "name", "postMessage", "userHex")


class UsersAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "username", "hex")


admin.site.register(Posts, PostsAdmin)
admin.site.register(Users, UsersAdmin)