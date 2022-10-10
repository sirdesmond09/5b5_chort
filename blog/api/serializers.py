from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        fields = ["title", "content", "date_posted", "slug"]


class UserSerialier(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ["pk", "username", "email"]


