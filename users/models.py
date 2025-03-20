from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    사용자 모델
    """
    email = models.EmailField(_('이메일 주소'), unique=True)
    profile_image = models.ImageField(
        _('프로필 이미지'), 
        upload_to='profile_images/', 
        null=True, 
        blank=True
    )
    profile_background = models.ImageField(
        _('프로필 배경'), 
        upload_to='profile_backgrounds/', 
        null=True, 
        blank=True
    )
    bio = models.TextField(_('자기소개'), blank=True)
    created_at = models.DateTimeField(_('가입일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    # 필수 필드 설정
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('사용자')
        verbose_name_plural = _('사용자')
        
    def __str__(self):
        return self.email


class UserInterest(models.Model):
    """
    사용자 관심사 모델
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='interests',
        verbose_name=_('사용자')
    )
    tag = models.CharField(_('관심 태그'), max_length=50)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('사용자 관심사')
        verbose_name_plural = _('사용자 관심사')
        unique_together = ('user', 'tag')
        
    def __str__(self):
        return f"{self.user.username} - {self.tag}"


class Follow(models.Model):
    """
    팔로우 관계 모델
    """
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following',
        verbose_name=_('팔로워')
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers',
        verbose_name=_('팔로잉')
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('팔로우')
        verbose_name_plural = _('팔로우')
        unique_together = ('follower', 'following')
        
    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"


class BlockedUser(models.Model):
    """
    차단된 사용자 모델
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blocked_users',
        verbose_name=_('사용자')
    )
    blocked_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blocked_by',
        verbose_name=_('차단된 사용자')
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('차단된 사용자')
        verbose_name_plural = _('차단된 사용자')
        unique_together = ('user', 'blocked_user')
        
    def __str__(self):
        return f"{self.user.username} blocked {self.blocked_user.username}"
