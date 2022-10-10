import imp
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from blog.models import Post


@api_view(["GET"])
def api_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


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






