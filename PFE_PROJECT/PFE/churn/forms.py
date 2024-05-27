from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SuperuserLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_superuser:
            raise forms.ValidationError(
                "Only superusers can access this page."
            )
