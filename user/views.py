from user.models import User
from .models import User, Image
from django.core.mail import EmailMessage
from decouple import config
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from django.utils import timezone
from kafka import KafkaProducer
from json import dumps
import datetime
import uuid
import hashlib
from django.http import HttpResponse
import requests

@api_view(["POST"])
def email(request):
    """
        비밀번호 리셋 이메일 발송

        @method     POST
        @header     
        @form-data  email
        @return     {"result": ""}
    """
    # 001. 이메일을 Body에서 가져옴
    email = request.data.get("email")

    try: 
        # 002. 이메일로 유저 객체를 가져옴
        user = User.objects.get(email=email)
    except:
        # 003. 이메일이 일치하는 Data가 없을 경우 404(Not Found) 리턴
        return JsonResponse({"result": config("USER_NONE")}, status=404)

    # 004. 토큰 생성. uuid4()는 32자리 랜덤 문자열을 생성해줌
    token = str(uuid.uuid4())
    # 005. 토큰을 암호화
    token_hashed = hashlib.sha256(token.encode("utf-8")).hexdigest()
    # 006. 토큰의 만료일 설정 (30분)
    expire = timezone.now() + datetime.timedelta(minutes=30)

    # 007. 유저 객체의 토큰 필드 설정
    user.password_reset_token = token_hashed
    # 008. 유저 객체의 토큰 만료일 필드 설정
    user.password_reset_token_expiration = expire
    # 009. 유저 객체 Update
    user.save(update_fields=["password_reset_token", "password_reset_token_expiration"])

    try:
        # 010. 이메일 객체 생성
        email_instance = EmailMessage(
            # 011. 이메일 제목
            subject="[AI-CHEMY] Password Reset Email", 
            # 012. 이메일 내용
            body=token,
            # 013. 이메일 전송 대상(배열이므로 전송 대상 다수 설정 가능)
            to=[user.email]
        )
        # 014. 이메일 전송
        email_instance.send()
    except:
        # 015. 이메일 전송 실패 시 408(Request Timeout) 리턴
        return JsonResponse({"result": config("EMAIL_FAIL")}, status=408)
    
    # 016. 이메일 전송 성공 시 200 리턴
    return JsonResponse({"result": config("EMAIL_SENT")}, status=200)

@api_view(["POST"])
def passwordReset(request):
    """
        비밀번호 리셋

        @method         POST
        @header     
        @form-data      email, uuid, password
        @return         {"result": ""}
    """

    # 001. 이메일, 토큰, 비밀번호를 BODY에서 가져옴
    email = request.data.get("email")
    token = request.data.get("uuid")
    password = request.data.get("password")

    # 002. 토큰이 없으면 400(Bad Request) 리턴
    if (token == None or token == ""):
        return JsonResponse({"result": config("TOKEN_NONE")}, status=400)
    
    # 003. Body에서 가져온 토큰을 암호화
    token_hashed = hashlib.sha256(token.encode("utf-8")).hexdigest()

    try:
        # 004. 이메일이 일치하는 데이터를 가져옴
        user = User.objects.get(email=email)
    except:
        # 005. 일치하는 데이터가 없으면 404(Not Found)
        return JsonResponse({"result": config("USER_NONE")}, status=404)
    
    # 006. 비밀번호 리셋을 요청한 적이 있는지 확인
    if (
        user.password_reset_token == None or 
        user.password_reset_token == "" or 
        user.password_reset_token_expiration == None or
        user.password_reset_token_expiration == ""
    ):
        # 007. 없으면 400(Bad Request) 리턴
        return JsonResponse({"result": config("PASSWORD_TOKEN_NONE")}, status=400)

    # 007. 입력한 토큰과 DB의 비밀번호 리셋 토큰이 일치하는지, 만료일이 지나지 않았는지 확인
    if (
        user.password_reset_token == token_hashed and
        user.password_reset_token_expiration > timezone.now()
    ):
        try:
            # 008. 유저 필드 설정하고 Validation 진행
            user.password = password
            user.password_reset_token = None
            user.password_reset_token_expiration = None
            user.full_clean()
        except:
            # 009. Validation 실패 시 409(Conflict) 리턴
            return JsonResponse({"result": config("PASSWORD_VALIDATION_FAIL")}, status=409)
        
        # 010. 비밀번호를 암호화하고 유저 객체 Update
        user.set_password(password)
        user.save(update_fields=["password", "password_reset_token", "password_reset_token_expiration"])

        return JsonResponse({"result": config("PASSWORD_CHANGED")}, status=200)
    else:
        # 011. 입력한 토큰이 일치하지 않거나, 토큰이 만료되었으면 401(Unauthorized) 리턴 
        return JsonResponse({"result": config("TOKEN_NOT_MATCH")}, status=401)

@api_view(["POST"])
def signup(request):
    """
        회원가입
        
        @method         POST
        @header
        @form-data      username, password, email
        @return         {"result": ""}
    """
    # 001. username, password, email을 Body에서 가져옴
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    # 002. 유저 객체 생성
    user = User(username=username, password=password, email=email)

    try:
        # 003. 유저 필드 Validation 후 비밀번호 암호화
        user.full_clean()
        user.set_password(password)
    except:
        # 004. Validation 실패 시 409(Conflict) 리턴
        return JsonResponse({"result": config("FIELD_VALIDATION_FAIL")}, status=409)
    
    # 005. Validation 성공 시 저장하고 200 리턴 
    user.save()
    return JsonResponse({"message": config("USER_CREATED")}, status=200)

@api_view(["POST"])
def getImgAddress(request):
    """
        유저 이미지 가져오기

        @method     POST
        @header     "Authorization": "Bearer " + 토큰값
        @form-data
        @return     {
                        "address": [
                            {
                                "1": "www.naver.com/abcd.png"
                            },
                            {
                                "2": "www.naver.com/efg.png"
                            }, ...
                        ]
                    }
    """
    # 001. header에서 토큰 값 가져와서 디코드
    JWT_authenticator = JWTAuthentication()
    # 002. 튜플 형태로 반환. response[0]은 <class 'user.models.User'>
    #       response[1]은 <class 'rest_framework_simplejwt.tokens.AccessToken'>
    response = JWT_authenticator.authenticate(request)

    # 003. 토큰 Payload에서 user_id 가져옴
    userid = response[1].get('user_id')

    # 004. 유저ID(FK)로 이미지들을 쿼리셋 형태로 가져옴
    userimg = Image.objects.filter(user_id_id=userid, is_deleted=False).values("address", "id")

    result = {"address": []}

    # 005. 쿼리셋에서 객체를 하나씩 가져온 후 결과값에 추가
    for imgObj in userimg:
        result["address"].append({imgObj.id: imgObj.address})

    # 006. 결과값 리턴
    return JsonResponse(result, status=200)

@api_view(["POST"])
def generateImage(request):
    """
        이미지 생성

        @method     POST
        @header     "authorization": "Bearer " + 토큰값
        @form-data  prompt
        @return     {"result": ""}
    """
    # 001. prompt를 Body에서 가져온 후 Validation
    prompt = request.data.get("prompt")
    if (prompt == None or prompt == ""):
        return JsonResponse({"result": config("PROMPT_NULL")}, status=400)

    # 002. JWT 토큰을 통해 유저 ID를 가져옴
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    userId = response[1].get("user_id")

    # 003. 유저ID로 유저 객체 가져옴
    user = User.objects.get(id=userId)
    
    # 004. Kafka 프로듀서 생성, 실패 시 408(Request Timeout) 리턴
    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
    except:
        return JsonResponse({"result": config("KAFKA_FAIL")}, status=408)

    

    # 005. DB에 address 필드가 null인 객체 생성
    image_instance = Image(user_id=user)
    image_instance.save()

    # 006. 카프카를 통해 보낼 JSON
    data = {
        "SECRET_KEY": config("FLASK_SECRET_KEY"),
        "username": user.username,
        "userid": user.id,
        "prompt": prompt,
        "imageid": image_instance.id
    }

    # 007. 카프카를 통해 데이터 전송, 첫번째 인자: TOPIC_NAME
    producer.send("image", value=data)

    return JsonResponse({
        "result": config("IMAGE_PROCESSING"),
        "image_id": image_instance.id
    }, status=200)

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

