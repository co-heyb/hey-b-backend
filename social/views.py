from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


@api_view(['GET'])
def post_list(request):
    """
    게시물 목록을 조회합니다.
    """
    paginator = PostPagination()
    posts = Post.objects.all()
    result_page = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(
        result_page, 
        many=True, 
        context={'request': request}
    )
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    """
    새 게시물을 생성합니다.
    """
    serializer = PostCreateSerializer(
        data=request.data, 
        context={'request': request}
    )
    if serializer.is_valid():
        post = serializer.save()
        return Response(
            PostSerializer(post, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def post_detail(request, post_id):
    """
    특정 게시물의 상세 정보를 조회합니다.
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {"detail": "게시물을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PostSerializer(post, context={'request': request})
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_post(request, post_id):
    """
    게시물을 수정합니다.
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {"detail": "게시물을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 본인 게시물만 수정 가능
    if post.user != request.user:
        return Response(
            {"detail": "이 게시물을 수정할 권한이 없습니다."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    """
    게시물을 삭제합니다.
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {"detail": "게시물을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 본인 게시물만 삭제 가능
    if post.user != request.user:
        return Response(
            {"detail": "이 게시물을 삭제할 권한이 없습니다."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
