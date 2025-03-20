from django.urls import path

from . import views

app_name = 'commerce'

urlpatterns = [
    # 카테고리 관리
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # 상품 관리
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path(
        'products/<slug:slug>/materials/',
        views.product_materials,
        name='product_materials'
    ),
    
    # 장바구니 관리
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # 주문 관리
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # 리뷰 관리
    path('products/<slug:slug>/reviews/', views.review_list, name='review_list'),
    path(
        'products/<slug:slug>/reviews/create/',
        views.create_review,
        name='create_review'
    ),
    path(
        'reviews/<int:review_id>/update/',
        views.update_review,
        name='update_review'
    ),
    path(
        'reviews/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review'
    ),
] 