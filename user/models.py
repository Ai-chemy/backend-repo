from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator

# # Create your models here.

class User(models.Model):
    user_key = models.IntegerField()
    
    username = models.CharField(max_length=15,validators=[MinLengthValidator(4), RegexValidator('^[a-z]+[a-z0-9]{3,14}$')])
    #최소 8 자, 최소 하나의 문자, 하나의 숫자 및 하나의 특수 문자 
    password = models.CharField(max_length=50, validators=[MinLengthValidator(8), RegexValidator('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')])
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField()
    generate_count = models.IntegerField()
    
    def __str__(self):
        return self.username
    
class Image(models.Model):
    image_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="image_id")
    address = models.URLField()
    
    def __str__(self):
        return self.address
