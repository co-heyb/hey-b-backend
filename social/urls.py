from django.urls import path

from . import views

app_name = 'social'

urlpatterns = [
    # 게시물 관리
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # 게시물 상호작용
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('posts/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('posts/<int:post_id>/unbookmark/', views.unbookmark_post, name='unbookmark_post'),
    
    # 댓글 관리
    path('posts/<int:post_id>/comments/', views.comment_list, name='comment_list'),
    path('posts/<int:post_id>/comments/create/', views.create_comment, name='create_comment'),
    path(
        'comments/<int:comment_id>/replies/create/',
        views.create_reply,
        name='create_reply'
    ),
    path('comments/<int:comment_id>/update/', views.update_comment, name='update_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # 해시태그 관리
    path('hashtags/', views.hashtag_list, name='hashtag_list'),
    path('hashtags/<str:name>/posts/', views.hashtag_posts, name='hashtag_posts'),
    
    # 피드
    path('feed/', views.feed, name='feed'),
    path('explore/', views.explore, name='explore'),
    path('bookmarks/', views.bookmarked_posts, name='bookmarked_posts'),
] 