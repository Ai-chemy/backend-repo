from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# Register your models here.

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password')

class MyUserAdmin(UserAdmin):
    list_display = (
        'user_key', 'username', 'password', 'email', 'created_at',
        'last_accessed_at', 'generate_count'
        )
    
    fieldsets  = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Important dates', {
            'fields': ('user_key', 'generate_count')
        }),
        ('Additional info', {
            'fields': ('created_at', 'last_accessed_at', 'email')
        })
    )

    add_fieldsets  = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Important dates', {
            'fields': ('user_key', 'generate_count')
        }),
        ('Additional info', {
            'fields': ('created_at', 'last_accessed_at', 'email')
        })
    )

admin.site.register(User)