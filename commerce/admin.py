from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Category, Product, ProductImage, ProductMaterial,
    Cart, CartItem, Order, OrderItem, Review, ReviewMedia
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductMaterialInline(admin.TabularInline):
    model = ProductMaterial
    extra = 1


class ReviewMediaInline(admin.TabularInline):
    model = ReviewMedia
    extra = 1


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'slug', 'price', 'discount_price', 'stock',
        'category', 'difficulty', 'is_active', 'created_at'
    )
    list_filter = ('is_active', 'difficulty', 'category', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [ProductImageInline, ProductMaterialInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'is_main', 'order', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('product__name',)
    ordering = ('product', 'order')


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'name')
    ordering = ('product', 'name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__user__username', 'product__name')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'status', 'total_price', 'payment_method',
        'shipping_name', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = (
        'user__username', 'user__email', 'shipping_name',
        'shipping_address', 'shipping_phone'
    )
    ordering = ('-created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__id', 'product__name')
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'product__name', 'content')
    ordering = ('-created_at',)
    inlines = [ReviewMediaInline]


@admin.register(ReviewMedia)
class ReviewMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('review__id', 'review__user__username', 'review__product__name')
    ordering = ('-created_at',)
