from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Post(models.Model):
    """
    게시물 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('작성자')
    )
    content = models.TextField(_('내용'))
    location = models.CharField(_('위치'), max_length=255, blank=True)
    created_at = models.DateTimeField(_('작성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('게시물')
        verbose_name_plural = _('게시물')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username}의 게시물 ({self.id})"


class PostMedia(models.Model):
    """
    게시물 미디어 모델
    """
    TYPE_CHOICES = (
        ('image', _('이미지')),
        ('video', _('동영상')),
    )
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name=_('게시물')
    )
    file = models.FileField(_('파일'), upload_to='post_media/')
    type = models.CharField(_('타입'), max_length=10, choices=TYPE_CHOICES)
    order = models.PositiveSmallIntegerField(_('순서'), default=0)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('게시물 미디어')
        verbose_name_plural = _('게시물 미디어')
        ordering = ['post', 'order']
        
    def __str__(self):
        return f"{self.post.id}의 {self.get_type_display()} ({self.id})"


class Hashtag(models.Model):
    """
    해시태그 모델
    """
    name = models.CharField(_('이름'), max_length=50, unique=True)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('해시태그')
        verbose_name_plural = _('해시태그')
        
    def __str__(self):
        return self.name


class PostHashtag(models.Model):
    """
    게시물-해시태그 연결 모델
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='hashtags',
        verbose_name=_('게시물')
    )
    hashtag = models.ForeignKey(
        Hashtag,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('해시태그')
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('게시물 해시태그')
        verbose_name_plural = _('게시물 해시태그')
        unique_together = ('post', 'hashtag')
        
    def __str__(self):
        return f"{self.post.id} - {self.hashtag.name}"


class Like(models.Model):
    """
    좋아요 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('사용자')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('게시물')
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('좋아요')
        verbose_name_plural = _('좋아요')
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username}가 {self.post.id}를 좋아합니다"


class Bookmark(models.Model):
    """
    북마크 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name=_('사용자')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name=_('게시물')
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('북마크')
        verbose_name_plural = _('북마크')
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username}가 {self.post.id}를 북마크했습니다"


class Comment(models.Model):
    """
    댓글 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('작성자')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('게시물')
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name=_('부모 댓글')
    )
    content = models.TextField(_('내용'))
    created_at = models.DateTimeField(_('작성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('댓글')
        verbose_name_plural = _('댓글')
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.user.username}의 댓글 ({self.id})"


class CommentMedia(models.Model):
    """
    댓글 미디어 모델
    """
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name=_('댓글')
    )
    image = models.ImageField(_('이미지'), upload_to='comment_images/')
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('댓글 미디어')
        verbose_name_plural = _('댓글 미디어')
        
    def __str__(self):
        return f"{self.comment.id}의 이미지 ({self.id})"
