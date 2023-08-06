from user.models import User
from .models import User, Image
from django.core.mail import EmailMessage
from decouple import config
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from django.utils import timezone
import uuid
import hashlib
from django.http import HttpResponse
import requests

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

@api_view(["POST"])
def getImgAddress(request):
    # """
    #     유저 이미지 가져오기
    #     @breif 토큰에서 유저아이디 가져와서 해당 유저가 생성한 이미지 주소들 반환
    # """

    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    
    #유저아이디
    userid = response[1].get('user_id')
    #유저ID 를 FK로 이미지 객체들을 가져옴
    userimg = Image.objects.filter(user_id_id=userid, is_deleted=False).values("address", "id")
    imginfo = []
    for image in userimg:
        info = {}
        info[image['id']] = image['address']
        imginfo.append(info)
    
    return JsonResponse({"address":imginfo}, status=200)

@api_view(["POST"])
def deleteImg(request):
    """
        이미지 삭제
        @brief "image_id"키로 삭제할 이미지 ID 전달하면 해당 이미지 is_deleted = True
    """

    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    imgid = request.data.get("image_id")

    #수행완료 response 1, 실패 response 0
    try:
        userimg = Image.objects.get(id=imgid)
    except Image.DoesNotExist:
        return JsonResponse({"response":0, "message":"Image does not exist"}, status=200)
    
    userimg.is_deleted = True
    userimg.save(update_fields=['is_deleted'])
    return JsonResponse({"response":1, "message":"delete image successfully"}, status=200)

@api_view(["POST"])
def singOut(request):
    """
        회원탈퇴

        @brief "user_id"키로 회원탈퇴 할 유저 ID 전달하면 해당 유저 is_active = False
    """

    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    userid = request.data.get("user_id")

    #수행완료 response 1, 실패 response 0
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        return JsonResponse({"response":0, "message":"User does not exist"}, status=200)
    
    user.is_active = False
    user.save(update_fields=['is_active'])
    return JsonResponse({"response":1, "message":"sign out successfully"}, status=200)

@api_view(["POST"])
def checkIdDuplication(request):
    """
        아이디 중복확인

        @brief "username"키로 데이터베이스에서 중복된 이름이 있는지 확인 후 결과 리턴
    """
    
    username = request.data.get("username")

    #중복안됨 response 1, 중복 response 0
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
       #중복된 ID가 아닐경우 reponse : 1
       return JsonResponse({"response":1, "message":"you can use this username"}, status=200)
    #중복된 ID일 경우 reponse : 0
    return JsonResponse({"response":0, "message":"this username already exist"}, status=200)

@api_view(["POST"])
def getImgData(request):
    """
        이미지 데이터 넘겨주기

        @brief url키에 있는 이미지의 데이터를 Bytes로 리턴
    """

    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    data = {
            "Content-Type": "application/json",
            "Authorization": "brandi.token"
    }

    requestUrl = request.data.get("url")

    imgData = requests.get(url=requestUrl, headers=data)
    return HttpResponse(imgData.content)



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

