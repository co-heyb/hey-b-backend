from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Post, PostMedia, Hashtag, PostHashtag, 
    Like, Bookmark, Comment, CommentMedia
)


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1


class PostHashtagInline(admin.TabularInline):
    model = PostHashtag
    extra = 1


class CommentMediaInline(admin.TabularInline):
    model = CommentMedia
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'content', 'location')
    ordering = ('-created_at',)
    inlines = [PostMediaInline, PostHashtagInline]


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'type', 'order', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('post__id', 'post__user__username')
    ordering = ('post', 'order')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(PostHashtag)
class PostHashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'hashtag', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__id', 'hashtag__name')
    ordering = ('-created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'post__id')
    ordering = ('-created_at',)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'post__id')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'parent', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'post__id', 'content')
    ordering = ('-created_at',)
    inlines = [CommentMediaInline]


@admin.register(CommentMedia)
class CommentMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment__id', 'comment__user__username')
    ordering = ('-created_at',)
