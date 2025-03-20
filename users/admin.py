from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserInterest, Follow, BlockedUser


class UserInterestInline(admin.TabularInline):
    model = UserInterest
    extra = 1


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('개인 정보'), {'fields': ('email', 'first_name', 'last_name')}),
        (_('프로필 정보'), {'fields': ('profile_image', 'profile_background', 'bio')}),
        (_('권한'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('중요 일자'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    inlines = [UserInterestInline]


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'tag')
    ordering = ('-created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'follower__email', 'following__username', 'following__email')
    ordering = ('-created_at',)


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'blocked_user__username', 'blocked_user__email')
    ordering = ('-created_at',)


admin.site.register(User, CustomUserAdmin)
