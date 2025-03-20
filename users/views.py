from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import UserInterest, Follow, BlockedUser
from .serializers import (
    UserSerializer, UserInterestSerializer, FollowSerializer, BlockedUserSerializer
)

User = get_user_model()


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    사용자 프로필 조회
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interest_list(request):
    """
    사용자 관심사 목록 조회
    """
    interests = UserInterest.objects.filter(user=request.user)
    serializer = UserInterestSerializer(interests, many=True)
    return Response(serializer.data)


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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_interest(request, interest_id):
    """
    사용자 관심사 삭제
    """
    interest = get_object_or_404(UserInterest, id=interest_id, user=request.user)
    interest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follower_list(request):
    """
    팔로워 목록 조회
    """
    followers = Follow.objects.filter(following=request.user)
    serializer = FollowSerializer(followers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    """
    팔로잉 목록 조회
    """
    following = Follow.objects.filter(follower=request.user)
    serializer = FollowSerializer(following, many=True)
    return Response(serializer.data)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blocked_user_list(request):
    """
    차단한 사용자 목록 조회
    """
    blocked_users = BlockedUser.objects.filter(user=request.user)
    serializer = BlockedUserSerializer(blocked_users, many=True)
    return Response(serializer.data)
