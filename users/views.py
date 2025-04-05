from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import UserInterest, Follow, BlockedUser
from .serializers import (
    UserSerializer, UserInterestSerializer, FollowSerializer, BlockedUserSerializer
)

User = get_user_model()

# 스웨거 응답 예시 정의
user_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='사용자 ID', example=1),
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 이름', example='johndoe'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일', example='john@example.com'),
        'profile_image': openapi.Schema(type=openapi.TYPE_STRING, description='프로필 이미지', example='https://hey-b.com/media/profile_images/johndoe.jpg'),
        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='자기소개', example='안녕하세요, 저는 존 도입니다.'),
        'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='가입일', example='2023-01-01T12:00:00Z'),
    }
)

interest_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='관심사 ID', example=1),
        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='사용자 ID', example=1),
        'interest': openapi.Schema(type=openapi.TYPE_STRING, description='관심사', example='목공예'),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성일', example='2023-01-01T12:00:00Z'),
    }
)

follow_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='팔로우 ID', example=1),
        'follower': openapi.Schema(type=openapi.TYPE_INTEGER, description='팔로워 ID', example=1),
        'following': openapi.Schema(type=openapi.TYPE_INTEGER, description='팔로잉 ID', example=2),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성일', example='2023-01-01T12:00:00Z'),
        'follower_username': openapi.Schema(type=openapi.TYPE_STRING, description='팔로워 이름', example='johndoe'),
        'following_username': openapi.Schema(type=openapi.TYPE_STRING, description='팔로잉 이름', example='janedoe'),
    }
)

blocked_user_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='차단 ID', example=1),
        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='사용자 ID', example=1),
        'blocked_user': openapi.Schema(type=openapi.TYPE_INTEGER, description='차단된 사용자 ID', example=3),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성일', example='2023-01-01T12:00:00Z'),
        'blocked_username': openapi.Schema(type=openapi.TYPE_STRING, description='차단된 사용자 이름', example='baduser'),
    }
)

@swagger_auto_schema(
    method='post',
    operation_description='사용자 회원가입을 처리합니다.',
    operation_summary='회원가입',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 이름', example='johndoe'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일', example='john@example.com'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호', example='securepassword123'),
            'profile_image': openapi.Schema(type=openapi.TYPE_STRING, description='프로필 이미지', example=None),
            'bio': openapi.Schema(type=openapi.TYPE_STRING, description='자기소개', example='안녕하세요, 저는 존 도입니다.'),
        }
    ),
    responses={
        201: openapi.Response(description='회원가입 성공', schema=user_response),
        400: '잘못된 요청',
    },
    tags=['사용자']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    사용자 회원가입
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description='현재 로그인한 사용자의 프로필을 조회합니다.',
    operation_summary='프로필 조회',
    responses={
        200: openapi.Response(description='프로필 조회 성공', schema=user_response),
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['사용자']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    사용자 프로필 조회
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@swagger_auto_schema(
    method='put',
    operation_description='현재 로그인한 사용자의 프로필을 수정합니다.',
    operation_summary='프로필 수정',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일', example='john.new@example.com'),
            'profile_image': openapi.Schema(type=openapi.TYPE_STRING, description='프로필 이미지', example=None),
            'bio': openapi.Schema(type=openapi.TYPE_STRING, description='자기소개', example='안녕하세요, 저는 존 도입니다. 취미는 여행입니다.'),
        }
    ),
    responses={
        200: openapi.Response(description='프로필 수정 성공', schema=user_response),
        400: '잘못된 요청',
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['사용자']
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    사용자 프로필 수정
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description='현재 로그인한 사용자의 관심사 목록을 조회합니다.',
    operation_summary='관심사 목록 조회',
    responses={
        200: openapi.Response(description='관심사 목록 조회 성공', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=interest_response
        )),
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['관심사']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interest_list(request):
    """
    사용자 관심사 목록 조회
    """
    interests = UserInterest.objects.filter(user=request.user)
    serializer = UserInterestSerializer(interests, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_description='현재 로그인한 사용자에게 관심사를 추가합니다.',
    operation_summary='관심사 추가',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['interest'],
        properties={
            'interest': openapi.Schema(type=openapi.TYPE_STRING, description='관심사', example='목공예'),
        }
    ),
    responses={
        201: openapi.Response(description='관심사 추가 성공', schema=interest_response),
        400: '잘못된 요청',
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['관심사']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_interest(request):
    """
    사용자 관심사 추가
    """
    serializer = UserInterestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_description='현재 로그인한 사용자의 관심사를 삭제합니다.',
    operation_summary='관심사 삭제',
    responses={
        204: '삭제 성공',
        401: '인증 실패',
        404: '관심사를 찾을 수 없습니다.',
    },
    security=[{'Bearer': []}],
    tags=['관심사']
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_interest(request, interest_id):
    """
    사용자 관심사 삭제
    """
    interest = get_object_or_404(UserInterest, id=interest_id, user=request.user)
    interest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='post',
    operation_description='다른 사용자를 팔로우합니다.',
    operation_summary='사용자 팔로우',
    responses={
        201: openapi.Response(description='팔로우 성공', schema=follow_response),
        400: '잘못된 요청 또는 이미 팔로우 중',
        401: '인증 실패',
        404: '사용자를 찾을 수 없습니다.',
    },
    security=[{'Bearer': []}],
    tags=['팔로우']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    """
    사용자 팔로우
    """
    user_to_follow = get_object_or_404(User, username=username)
    
    # 자기 자신을 팔로우할 수 없음
    if request.user == user_to_follow:
        return Response(
            {"detail": "자기 자신을 팔로우할 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 이미 팔로우 중인지 확인
    if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        return Response(
            {"detail": "이미 팔로우 중입니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    follow = Follow.objects.create(follower=request.user, following=user_to_follow)
    serializer = FollowSerializer(follow)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='delete',
    operation_description='팔로우 중인 사용자를 언팔로우합니다.',
    operation_summary='사용자 언팔로우',
    responses={
        204: '언팔로우 성공',
        401: '인증 실패',
        404: '사용자를 찾을 수 없거나 팔로우 중이 아닙니다.',
    },
    security=[{'Bearer': []}],
    tags=['팔로우']
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, username):
    """
    사용자 언팔로우
    """
    user_to_unfollow = get_object_or_404(User, username=username)
    follow = get_object_or_404(
        Follow, follower=request.user, following=user_to_unfollow
    )
    follow.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_description='현재 로그인한 사용자를 팔로우하는 사용자(팔로워) 목록을 조회합니다.',
    operation_summary='팔로워 목록 조회',
    responses={
        200: openapi.Response(description='팔로워 목록 조회 성공', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=follow_response
        )),
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['팔로우']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follower_list(request):
    """
    팔로워 목록 조회
    """
    followers = Follow.objects.filter(following=request.user)
    serializer = FollowSerializer(followers, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_description='현재 로그인한 사용자가 팔로우하는 사용자(팔로잉) 목록을 조회합니다.',
    operation_summary='팔로잉 목록 조회',
    responses={
        200: openapi.Response(description='팔로잉 목록 조회 성공', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=follow_response
        )),
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['팔로우']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    """
    팔로잉 목록 조회
    """
    following = Follow.objects.filter(follower=request.user)
    serializer = FollowSerializer(following, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_description='다른 사용자를 차단합니다.',
    operation_summary='사용자 차단',
    responses={
        201: openapi.Response(description='차단 성공', schema=blocked_user_response),
        400: '잘못된 요청 또는 이미 차단 중',
        401: '인증 실패',
        404: '사용자를 찾을 수 없습니다.',
    },
    security=[{'Bearer': []}],
    tags=['차단']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_user(request, username):
    """
    사용자 차단
    """
    user_to_block = get_object_or_404(User, username=username)
    
    # 자기 자신을 차단할 수 없음
    if request.user == user_to_block:
        return Response(
            {"detail": "자기 자신을 차단할 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 이미 차단 중인지 확인
    if BlockedUser.objects.filter(
        user=request.user, blocked_user=user_to_block
    ).exists():
        return Response(
            {"detail": "이미 차단 중입니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 팔로우 관계가 있다면 삭제
    Follow.objects.filter(
        follower=request.user, following=user_to_block
    ).delete()
    Follow.objects.filter(
        follower=user_to_block, following=request.user
    ).delete()
    
    blocked = BlockedUser.objects.create(
        user=request.user, blocked_user=user_to_block
    )
    serializer = BlockedUserSerializer(blocked)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='delete',
    operation_description='차단 중인 사용자의 차단을 해제합니다.',
    operation_summary='사용자 차단 해제',
    responses={
        204: '차단 해제 성공',
        401: '인증 실패',
        404: '사용자를 찾을 수 없거나 차단 중이 아닙니다.',
    },
    security=[{'Bearer': []}],
    tags=['차단']
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unblock_user(request, username):
    """
    사용자 차단 해제
    """
    user_to_unblock = get_object_or_404(User, username=username)
    blocked = get_object_or_404(
        BlockedUser, user=request.user, blocked_user=user_to_unblock
    )
    blocked.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_description='현재 로그인한 사용자가 차단한 사용자 목록을 조회합니다.',
    operation_summary='차단 사용자 목록 조회',
    responses={
        200: openapi.Response(description='차단 사용자 목록 조회 성공', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=blocked_user_response
        )),
        401: '인증 실패',
    },
    security=[{'Bearer': []}],
    tags=['차단']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blocked_user_list(request):
    """
    차단한 사용자 목록 조회
    """
    blocked_users = BlockedUser.objects.filter(user=request.user)
    serializer = BlockedUserSerializer(blocked_users, many=True)
    return Response(serializer.data)
