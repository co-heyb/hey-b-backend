from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, PostMedia, Hashtag, PostHashtag

User = get_user_model()


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['id', 'file', 'type', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'username', 'content', 'location', 
            'created_at', 'updated_at', 'media', 'likes_count', 
            'comments_count', 'is_liked', 'is_bookmarked'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, required=False)
    hashtags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['content', 'location', 'media', 'hashtags']
    
    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtags', [])
        media_data = validated_data.pop('media', [])
        
        # 게시물 생성
        post = Post.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        
        # 해시태그 처리
        for tag_name in hashtags_data:
            tag_name = tag_name.strip().lower()
            if tag_name:
                hashtag, _ = Hashtag.objects.get_or_create(name=tag_name)
                PostHashtag.objects.create(post=post, hashtag=hashtag)
        
        # 미디어 처리
        for media_item in media_data:
            PostMedia.objects.create(post=post, **media_item)
        
        return post 