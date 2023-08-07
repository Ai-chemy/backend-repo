from django.db import models
from django.core.validators import MinLengthValidator , RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        username = User.normalize_username(username)
        user = User(username=username, email=email, password=password, **extra_fields)
        try:
            user.full_clean()
        except Exception as e:
            print(e)
        else:
            user.set_password(password)
            user.save()
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(4), RegexValidator('^[a-zA-Z0-9]{4,14}$')])
    #최소 8 자, 최소 하나의 문자, 하나의 숫자 및 하나의 특수 문자 
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8), RegexValidator('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')])
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    generate_count = models.IntegerField(default=0)
    password_reset_token = models.CharField(max_length=150, null=True, blank=True, default=None)
    password_reset_token_expiration = models.DateTimeField(null=True, blank=True, default=None)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    #views.py에서 User의 정보를 얻을때 사용 ex)user = User.objects.get(username="office54")
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.username
    
class Image(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    address = models.URLField(null=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.address