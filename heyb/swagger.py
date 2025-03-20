from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView as OriginalTokenObtainPairView,
    TokenRefreshView as OriginalTokenRefreshView,
    TokenVerifyView as OriginalTokenVerifyView,
)
from django.urls import path

# JWT 인증을 위한 스웨거 데코레이터 설정
token_obtain_pair_schema = swagger_auto_schema(
    operation_description="JWT 액세스 토큰과 리프레시 토큰을 발급받습니다.",
    responses={
        200: "토큰 발급 성공",
        400: "잘못된 요청",
        401: "인증 실패"
    },
    security=[],
    tags=['인증']
)

token_refresh_schema = swagger_auto_schema(
    operation_description="리프레시 토큰을 사용하여 새 액세스 토큰을 발급받습니다.",
    responses={
        200: "토큰 갱신 성공",
        400: "잘못된 요청",
        401: "인증 실패"
    },
    security=[],
    tags=['인증']
)

token_verify_schema = swagger_auto_schema(
    operation_description="토큰의 유효성을 검증합니다.",
    responses={
        200: "유효한 토큰",
        400: "잘못된 요청",
        401: "인증 실패"
    },
    security=[],
    tags=['인증']
)

# 토큰 뷰에 스웨거 데코레이터 적용
class TokenObtainPairView(OriginalTokenObtainPairView):
    @token_obtain_pair_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TokenRefreshView(OriginalTokenRefreshView):
    @token_refresh_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TokenVerifyView(OriginalTokenVerifyView):
    @token_verify_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# API 문서화 설정
schema_view = get_schema_view(
    openapi.Info(
        title="HeyB API",
        default_version='v1',
        description=(
            "취미 활동 공유 및 취미키트 구매 플랫폼 API\n\n"
            "## 인증 방법\n"
            "1. `/api/users/token/` 엔드포인트에서 사용자 이름과 비밀번호로 토큰을 발급받습니다.\n"
            "2. 응답으로 받은 `access` 토큰을 Authorize 버튼을 클릭하여 입력합니다.\n"
            "3. 토큰 앞에 `Bearer `를 붙이지 마세요. 자동으로 추가됩니다."
        ),
        terms_of_service="https://www.heyb.com/terms/",
        contact=openapi.Contact(email="contact@heyb.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 아래 urlpatterns 추가
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] 