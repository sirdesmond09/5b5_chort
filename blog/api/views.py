from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import PostSerializer, UserRegistrationSerializer, UserPropertiesSerializer
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

@api_view(["GET", "POST"])
def api_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        user = request.user
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



@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated))
def api_detail_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        data = {}
        operation = post.delete()
        if operation:
            data["Success"] = "Post delete successful"
        else:
            data["Failure"] = "Post delete failed"
        return Response(data=data)


@api_view(["PUT"])
@permission_classes((IsAuthenticated))
def api_update_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user != post.author:
        return Response({"Error": "You cannot update a post you didn't create"})

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data["Success"] = "Blog updated successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes((IsAuthenticated))
def api_delete_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user != post.author:
        return Response({"Error": "You cannot delete a post you didn't create"})
    
    if request.method == "DELETE":
        data = {}
        operation = post.delete()
        if operation:
            data["Success"] = "Post delete successful"
        else:
            data["Failure"] = "Post delete failed"
        return Response(data=data)

    
@api_view(["POST"])
@permission_classes((IsAuthenticated))
def api_create_view(request):
    user = request.user
    post = Post(author=user)

    if request.method == "POST":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def api_register_view(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["Success"] = "User creation successful"
            data["username"] = user.username
            data["email"] = user.email
            token = Token.objects.get(user=user).key
            data["token"] = token
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["title", "content", "slug", "author__username"]


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_user_properties(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserPropertiesSerializer(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def api_update_user_properties(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = UserPropertiesSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            updated_post = serializer.save()
            data["success"] = "Account update successful"
            data["username"] = updated_post.username
            data["email"] = updated_post.email
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










