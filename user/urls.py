from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.sendEmail, name = 'sendEmail')
]
