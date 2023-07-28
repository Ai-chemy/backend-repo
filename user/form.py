from django.contrib.auth.forms import SetPasswordForm
from django import forms
from django.contrib.auth import password_validation
from django.core.validators import MinLengthValidator , RegexValidator
from django.utils.translation import gettext_lazy as _

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        validators=[MinLengthValidator(8), RegexValidator('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')]
    )