from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Image

class UserCreationForm(forms.ModelForm):
    # A form for creating new users. 
    # Includes all the required fields, plus a repeated password.

    class Meta:
        model = User
        fields = "__all__"

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    # A form for updating users. Includes all the fields on
    # the user, but replaces the password field with admin's
    # disabled password hash display field.
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["username", "created_at"]
    list_filter = ["is_superuser"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["last_login"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "fields": ["username", "password", "email"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(User, UserAdmin)
admin.site.register(Image)