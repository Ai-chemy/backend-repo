from django.test import TestCase
from .models import User
from datetime import datetime

# Create your tests here.
class UserCreationTests(TestCase):
    def test_username_is_short(self):
        now = datetime.now()
        min_test = "aaa"
        test1 = User.objects.create(
            username=min_test, 
            password="1234", 
            created_at=now
        )
        
    def test_username_is_long(self):
        now = datetime.now()
        max_test = "aaaaaaaaaaaaaaaa"
        test2 = User.objects.create(
            username=max_test, 
            password="1234",
            created_at=now
        )
    