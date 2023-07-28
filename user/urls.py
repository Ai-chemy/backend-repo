from django.urls import path, include

from . import views
urlpatterns = [
    path('email/', views.onlyAuthenticate.sendEmail, name = 'sendEmail'),
    path('signup/', views.onlyAuthenticate.signUp, name = 'signUp')
]
