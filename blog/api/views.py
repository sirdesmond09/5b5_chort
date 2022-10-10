from operator import is_
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer, UserSerializer
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model

@api_view(["GET", "POST"])
def api_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        user = User.objects.get(pk=1)
        post = Post(author=user)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            data = {}
            new_post = serializer.save()
            data["Response"] = "Post creation successful"
            data["title"] = new_post.title
            data["content"] = new_post.content
            data["date_posted"] = new_post.date_posted
            data["slug"] = new_post.slug
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def api_detail_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)


@api_view(["PUT"])
def api_update_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data["Success"] = "Blog updated successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def api_delete_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        data = {}
        operation = post.delete()
        if operation:
            data["Success"] = "Post delete successful"
        else:
            data["Failure"] = "Post delete failed"
        return Response(data=data)

    
@api_view(["POST"])
def api_create_view(request):
    user = User.objects.get(pk=1)
    post = Post(author=user)

    if request.method == "POST":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








