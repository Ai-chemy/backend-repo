from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# # Create your models here.
# class User(models.Model):
#     # username = models.CharField(max_length=15, validators=[MinValueValidator(4)])
#     username = models.CharField(max_length=15)
#     password = models.CharField(max_length=50)
#     created_at = models.DateTimeField()

# 새로운 모델 작성 필요