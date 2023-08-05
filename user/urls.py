from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
urlpatterns = [
    # 회원가입
    path('signup/', views.signup, name = 'signUp'),
    # Token 발급
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    # Token 재발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 비밀번호 리셋 이메일 발송
    path("email/", views.email, name="email"),
    # 비밀번호 리셋
    path("reset/", views.passwordReset, name="reset"),
    # 이미지 GET
    path("getimg/", views.getImg, name='getImg'),
    # 이미지생성
    path("generate/", views.generateImage, name="generate"),
    # 테스트용
    path("test/", views.test, name="asdasd"),
]
