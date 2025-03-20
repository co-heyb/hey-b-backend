from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Category(models.Model):
    """
    카테고리 모델
    """
    name = models.CharField(_('이름'), max_length=100)
    slug = models.SlugField(_('슬러그'), unique=True)
    description = models.TextField(_('설명'), blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('상위 카테고리')
    )
    image = models.ImageField(
        _('이미지'),
        upload_to='category_images/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('카테고리')
        verbose_name_plural = _('카테고리')
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    상품 모델
    """
    DIFFICULTY_CHOICES = (
        ('beginner', _('초급')),
        ('intermediate', _('중급')),
        ('advanced', _('고급')),
    )
    
    name = models.CharField(_('이름'), max_length=200)
    slug = models.SlugField(_('슬러그'), unique=True)
    description = models.TextField(_('설명'))
    price = models.DecimalField(_('가격'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        _('할인 가격'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    stock = models.PositiveIntegerField(_('재고'))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('카테고리')
    )
    difficulty = models.CharField(
        _('난이도'),
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner'
    )
    estimated_time = models.PositiveIntegerField(_('예상 소요시간(분)'))
    is_active = models.BooleanField(_('활성화 여부'), default=True)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('상품')
        verbose_name_plural = _('상품')
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    상품 이미지 모델
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('상품')
    )
    image = models.ImageField(_('이미지'), upload_to='product_images/')
    is_main = models.BooleanField(_('대표 이미지 여부'), default=False)
    order = models.PositiveSmallIntegerField(_('순서'), default=0)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('상품 이미지')
        verbose_name_plural = _('상품 이미지')
        ordering = ['product', 'order']
        
    def __str__(self):
        return f"{self.product.name}의 이미지 ({self.id})"


class ProductMaterial(models.Model):
    """
    상품 재료 모델
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name=_('상품')
    )
    name = models.CharField(_('재료명'), max_length=100)
    quantity = models.CharField(_('수량'), max_length=50)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('상품 재료')
        verbose_name_plural = _('상품 재료')
        
    def __str__(self):
        return f"{self.product.name}의 재료: {self.name}"


class Cart(models.Model):
    """
    장바구니 모델
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('사용자')
    )
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('장바구니')
        verbose_name_plural = _('장바구니')
        
    def __str__(self):
        return f"{self.user.username}의 장바구니"


class CartItem(models.Model):
    """
    장바구니 아이템 모델
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('장바구니')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('상품')
    )
    quantity = models.PositiveIntegerField(_('수량'), default=1)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('장바구니 아이템')
        verbose_name_plural = _('장바구니 아이템')
        unique_together = ('cart', 'product')
        
    def __str__(self):
        return f"{self.cart.user.username}의 장바구니: {self.product.name} x {self.quantity}"


class Order(models.Model):
    """
    주문 모델
    """
    STATUS_CHOICES = (
        ('pending', _('결제 대기')),
        ('paid', _('결제 완료')),
        ('shipping', _('배송 중')),
        ('delivered', _('배송 완료')),
        ('cancelled', _('취소')),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('사용자')
    )
    status = models.CharField(
        _('상태'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    shipping_address = models.TextField(_('배송 주소'))
    shipping_name = models.CharField(_('수령인'), max_length=100)
    shipping_phone = models.CharField(_('연락처'), max_length=20)
    shipping_memo = models.TextField(_('배송 메모'), blank=True)
    total_price = models.DecimalField(_('총 금액'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('결제 방법'), max_length=50)
    tracking_number = models.CharField(
        _('운송장 번호'),
        max_length=50,
        blank=True
    )
    created_at = models.DateTimeField(_('주문일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('주문')
        verbose_name_plural = _('주문')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username}의 주문 ({self.id})"


class OrderItem(models.Model):
    """
    주문 아이템 모델
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('주문')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('상품')
    )
    quantity = models.PositiveIntegerField(_('수량'))
    price = models.DecimalField(_('가격'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('주문 아이템')
        verbose_name_plural = _('주문 아이템')
        
    def __str__(self):
        return f"{self.order.id}의 아이템: {self.product.name} x {self.quantity}"


class Review(models.Model):
    """
    리뷰 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('사용자')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('상품')
    )
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='review',
        verbose_name=_('주문 아이템')
    )
    rating = models.PositiveSmallIntegerField(_('평점'), choices=[(i, i) for i in range(1, 6)])
    content = models.TextField(_('내용'))
    created_at = models.DateTimeField(_('작성일'), auto_now_add=True)
    updated_at = models.DateTimeField(_('수정일'), auto_now=True)
    
    class Meta:
        verbose_name = _('리뷰')
        verbose_name_plural = _('리뷰')
        ordering = ['-created_at']
        unique_together = ('user', 'product')
        
    def __str__(self):
        return f"{self.user.username}의 {self.product.name} 리뷰"


class ReviewMedia(models.Model):
    """
    리뷰 미디어 모델
    """
    TYPE_CHOICES = (
        ('image', _('이미지')),
        ('video', _('동영상')),
    )
    
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name=_('리뷰')
    )
    file = models.FileField(_('파일'), upload_to='review_media/')
    type = models.CharField(_('타입'), max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(_('생성일'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('리뷰 미디어')
        verbose_name_plural = _('리뷰 미디어')
        
    def __str__(self):
        return f"{self.review.id}의 {self.get_type_display()} ({self.id})"
