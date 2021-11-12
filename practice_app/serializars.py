from rest_framework import serializers
from .models import  Posts, Users

# SERIALIZERS CONVERT DATA TO JSON

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ("timestamp", "postId", "username", "name", "postMessage", "userHex")

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("name", "email", "username", "hex")
