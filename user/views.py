from user.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from django.core.mail import EmailMessage
from decouple import config
from django.http import HttpResponse
# Create your views here.

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

def sendEmail(request): 
    email = EmailMessage(
        'This is password email', #이메일 제목
        'testtest', #내용
        to=[config('EMAIL')], #받는 이메일
    )
    email.send()
    return HttpResponse('We Have Sent Our Email')