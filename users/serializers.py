from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserInterest, Follow, BlockedUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    사용자 시리얼라이저
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'profile_image', 'profile_background', 'bio', 'date_joined',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'date_joined', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        return user


class UserInterestSerializer(serializers.ModelSerializer):
    """
    사용자 관심사 시리얼라이저
    """
    class Meta:
        model = UserInterest
        fields = ('id', 'user', 'tag', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class FollowSerializer(serializers.ModelSerializer):
    """
    팔로우 시리얼라이저
    """
    follower_detail = UserSerializer(source='follower', read_only=True)
    following_detail = UserSerializer(source='following', read_only=True)
    
    class Meta:
        model = Follow
        fields = (
            'id', 'follower', 'following', 'follower_detail',
            'following_detail', 'created_at'
        )
        read_only_fields = ('id', 'follower', 'following', 'created_at')


class BlockedUserSerializer(serializers.ModelSerializer):
    """
    차단된 사용자 시리얼라이저
    """
    user_detail = UserSerializer(source='user', read_only=True)
    blocked_user_detail = UserSerializer(source='blocked_user', read_only=True)
    
    class Meta:
        model = BlockedUser
        fields = (
            'id', 'user', 'blocked_user', 'user_detail',
            'blocked_user_detail', 'created_at'
        )
        read_only_fields = ('id', 'user', 'blocked_user', 'created_at') 