from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# 스웨거 응답 예시 정의
post_list_response = openapi.Response(
    description='게시물 목록 조회 성공',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='총 게시물 수'),
            'next': openapi.Schema(type=openapi.TYPE_STRING, description='다음 페이지 URL', nullable=True),
            'previous': openapi.Schema(type=openapi.TYPE_STRING, description='이전 페이지 URL', nullable=True),
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='게시물 ID'),
                        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='작성자 ID'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='작성자 이름'),
                        'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시물 내용'),
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='위치'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='작성일'),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정일'),
                        'likes_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='좋아요 수'),
                        'comments_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='댓글 수'),
                        'is_liked': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='현재 사용자의 좋아요 여부'),
                        'is_bookmarked': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='현재 사용자의 북마크 여부'),
                        'media': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='미디어 ID'),
                                    'file': openapi.Schema(type=openapi.TYPE_STRING, description='파일 URL'),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='미디어 타입'),
                                    'order': openapi.Schema(type=openapi.TYPE_INTEGER, description='순서'),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성일'),
                                }
                            )
                        ),
                    }
                )
            )
        }
    )
)

# 게시물 상세 응답 예시
post_detail_response = openapi.Response(
    description='게시물 상세 조회 성공',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='게시물 ID'),
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='작성자 ID'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='작성자 이름'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시물 내용'),
            'location': openapi.Schema(type=openapi.TYPE_STRING, description='위치'),
            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='작성일'),
            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정일'),
            'likes_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='좋아요 수'),
            'comments_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='댓글 수'),
            'is_liked': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='현재 사용자의 좋아요 여부'),
            'is_bookmarked': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='현재 사용자의 북마크 여부'),
            'media': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='미디어 ID'),
                        'file': openapi.Schema(type=openapi.TYPE_STRING, description='파일 URL'),
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description='미디어 타입'),
                        'order': openapi.Schema(type=openapi.TYPE_INTEGER, description='순서'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성일'),
                    }
                )
            ),
        }
    )
)

# 게시물 생성 요청 예시
post_create_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['content'],
    properties={
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시물 내용'),
        'location': openapi.Schema(type=openapi.TYPE_STRING, description='위치', default=''),
        'hashtags': openapi.Schema(
            type=openapi.TYPE_ARRAY, 
            items=openapi.Schema(type=openapi.TYPE_STRING),
            description='해시태그 목록'
        ),
        'media': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'file': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='파일'),
                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='미디어 타입 (image, video)'),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER, description='순서', default=0),
                }
            ),
            description='미디어 목록'
        ),
    }
)


@swagger_auto_schema(
    method='get',
    operation_description='게시물 목록을 조회합니다.',
    operation_summary='게시물 목록 조회',
    responses={200: post_list_response},
    tags=['게시물']
)
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


@swagger_auto_schema(
    method='post',
    operation_description='새 게시물을 생성합니다.',
    operation_summary='게시물 생성',
    request_body=post_create_request,
    responses={
        201: post_detail_response,
        400: '잘못된 요청',
        401: '인증 실패'
    },
    security=[{'Bearer': []}],
    tags=['게시물']
)
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


@swagger_auto_schema(
    method='get',
    operation_description='특정 게시물의 상세 정보를 조회합니다.',
    operation_summary='게시물 상세 조회',
    responses={
        200: post_detail_response,
        404: '게시물을 찾을 수 없습니다.'
    },
    tags=['게시물']
)
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


@swagger_auto_schema(
    method='put',
    operation_description='게시물을 수정합니다.',
    operation_summary='게시물 수정 (전체)',
    request_body=post_create_request,
    responses={
        200: post_detail_response,
        400: '잘못된 요청',
        401: '인증 실패',
        403: '권한 없음',
        404: '게시물을 찾을 수 없습니다.'
    },
    security=[{'Bearer': []}],
    tags=['게시물']
)
@swagger_auto_schema(
    method='patch',
    operation_description='게시물을 부분 수정합니다.',
    operation_summary='게시물 수정 (부분)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시물 내용'),
            'location': openapi.Schema(type=openapi.TYPE_STRING, description='위치'),
        }
    ),
    responses={
        200: post_detail_response,
        400: '잘못된 요청',
        401: '인증 실패',
        403: '권한 없음',
        404: '게시물을 찾을 수 없습니다.'
    },
    security=[{'Bearer': []}],
    tags=['게시물']
)
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


@swagger_auto_schema(
    method='delete',
    operation_description='게시물을 삭제합니다.',
    operation_summary='게시물 삭제',
    responses={
        204: '삭제 성공',
        401: '인증 실패',
        403: '권한 없음',
        404: '게시물을 찾을 수 없습니다.'
    },
    security=[{'Bearer': []}],
    tags=['게시물']
)
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
