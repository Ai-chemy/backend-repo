from user.models import User
from .models import User
from django.core.mail import EmailMessage
from decouple import config
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from django.utils import timezone
import uuid
import hashlib

@api_view(["POST"])
def email(request):
    """
        비밀번호 리셋 이메일 발송

        추가설명  
    """
    email = request.data.get("email")
    user = None

    try: 
        user = User.objects.get(email=email)
    except Exception as e:
        print(e)

    if (user):
        token = str(uuid.uuid4())
        token_hashed = hashlib.sha256(token.encode("utf-8")).hexdigest()
        expire = timezone.now()
        # + datetime.timedelta(minutes=30)

        try:
            user.password_reset_token = token_hashed
            user.password_reset_token_expiration = expire
            user.save(update_fields=["password_reset_token", "password_reset_token_expiration"])
        except Exception as e:
            print(e)

        try:
            email_instance = EmailMessage(
                subject="[AI-CHEMY] Password Reset Email", 
                body=token,
                to=[user.email]
            )
            email_instance.send()
        except Exception as e:
            print(e)

    return JsonResponse({"a":"b"}, status=200)

@api_view(["POST"])
def signup(request):
    """
        회원가입
        
        username, password, email을 body로 부터 가져와서 Validation후 DB에 저장
    """
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    user = User(username=username, password=password, email=email)

    try:
        # full_clean() 메소드는 
        # Model.clean_fields(), Model,clean(), Model.validate_unique() 3개의 메소드를 연달아 호출하는데
        # clean_fields(): 모델에 정의한 field들을 검증하며, 통과하지 못하면 ValidationError를 발생시킴
        # clean(): clean() 메소드 안에 정의한 사용자 정의 Validation을 검증
        # validate_unique(): unique를 설정해놓은 필드들을 검증 
        user.full_clean()
        user.set_password(password)
    except Exception as e:
        data = {
            "message" : "USER_CREATION_FAILED", 
            "status" : e.message_dict
        }

        return JsonResponse(data, status=409)
    else:
        user.save()

    return JsonResponse({"message":"USER_CREATED"}, status=200)

# --------------------------------------------------------------------------

@api_view(["POST"])
def test(request):
    print(request.headers)
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)

    print(response)
    print(str(response))

    return JsonResponse({}, status=200)

@api_view(["POST"])
def password(request):
    pass