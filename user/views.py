from user.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from django.core.mail import EmailMessage
from decouple import config
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class onlyAuthenticate():
    @csrf_exempt
    #@api view get
    #@permission_class(isauthenticated)
    def sendEmail(request):
        if request.method == "POST":
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                mail_data = json.loads(request.body)
                try:
                    mail_title = mail_data['title']
                    mail_content = mail_data['content']
                    mail_receiver = mail_data['receiver']
                    email = EmailMessage(
                        mail_title, #이메일 제목
                        mail_content, #내용
                        to=[mail_receiver], #받는 이메일
                    )
                    email.send()
                    return HttpResponse('We Have Sent Our Email')
                except KeyError:
                    return JsonResponse({"message": "KeyError"}, status=400)
            else:
                    return HttpResponse("no token is provided in the header or the header is missing")
        else:
             return JsonResponse({"message": "METHOD ERROR"}, status=400)

    @csrf_exempt
    def signUp(request):
        if request.method == "POST":
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                signup_data = json.loads(request.body)
                try:
                    username = signup_data['username']
                    email = signup_data['email']
                    password = signup_data['password']
                    User.objects.create_user(username, email, password)
                    return HttpResponse("you have signed up as Username : " + username)
                except KeyError:
                        return JsonResponse({"message": "KeyError"}, status=400)
            else:
                return HttpResponse("no token is provided in the header or the header is missing")
        else:
             return JsonResponse({"message": "METHOD ERROR"}, status=400)