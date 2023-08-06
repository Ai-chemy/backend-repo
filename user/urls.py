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
    # 비밀번호 리셋 이메일 발송, 현재 작성중
    path("email/", views.email, name="asdasd"),
    # 테스트용
    path("test/", views.test, name="asdasd"),
    # 이미지 주소 GET
    path("getimgaddress/", views.getImgAddress, name='getImgAddress'),
    # 이미지 DELETE
    path("deleteimg/", views.deleteImg, name='deleteImg'),
    # 회원탈퇴
    path("signout/", views.singOut, name='signOut'),
    # 아이디중복확인
    path("checkduplication/", views.checkIdDuplication, name='checkIdDuplication'),
    # 이미지 데이터 GET
    path("getimgdata/", views.getImgData, name='getImgData')
]
