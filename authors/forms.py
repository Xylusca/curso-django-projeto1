import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")
    if not regex.match(password):
        raise ValidationError(
            (
                "The password must have at least: "
                "One uppercase letter, "
                "One lowercase letter, "
                "One number, "
                "Eight characters."
            ),
            code="invalid",
        )


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat your password",
                "class": "form-control",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Type your password",
            }
        ),
        error_messages={"required": "Password must not be empty"},
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters."
        ),
        validators=[strong_password],
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control input-register",
                    "placeholder": "Ex.: Lucas",
                }
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex.: Pereira"}
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your e-mail"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError(
                {
                    "password": "The entered passwords do not match. Please try again.",
                    "password2": "The entered passwords do not match. Please try again.",
                }
            )
