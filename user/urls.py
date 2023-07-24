from django.urls import path, include

from . import views
urlpatterns = [
    path('email/', views.sendEmail, name = 'sendEmail'),
    path('signup/', views.signUp, name = 'signUp')
]
