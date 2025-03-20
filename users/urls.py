from django.urls import path
from heyb.swagger import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

app_name = 'users'

urlpatterns = [
    # JWT 인증
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 사용자 관리
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # 관심사 관리
    path('interests/', views.interest_list, name='interest_list'),
    path('interests/add/', views.add_interest, name='add_interest'),
    path('interests/<int:interest_id>/delete/', views.delete_interest, name='delete_interest'),
    
    # 팔로우 관리
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('followers/', views.follower_list, name='follower_list'),
    path('following/', views.following_list, name='following_list'),
    
    # 차단 관리
    path('block/<str:username>/', views.block_user, name='block_user'),
    path('unblock/<str:username>/', views.unblock_user, name='unblock_user'),
    path('blocked/', views.blocked_user_list, name='blocked_user_list'),
] 