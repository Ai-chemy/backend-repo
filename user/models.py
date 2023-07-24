from django.db import models
from django.core.validators import MinLengthValidator , RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# # Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('username을 입력해주세요.')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=True일 필요가 있습니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=True일 필요가 있습니다.')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # = user_key = id
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(4), RegexValidator('^[a-z]+[a-z0-9]{3,14}$')])
    #최소 8 자, 최소 하나의 문자, 하나의 숫자 및 하나의 특수 문자 
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8), RegexValidator('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')])
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_accessed_at = models.DateTimeField(default=timezone.now)
    generate_count = models.IntegerField(default=0)

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    
    #views.py에서 User의 정보를 얻을때 사용 ex)user = User.objects.get(username="office54")
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.username
    
class Image(models.Model):
    image_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="image_id")
    address = models.URLField()
    
    def __str__(self):
        return self.address
