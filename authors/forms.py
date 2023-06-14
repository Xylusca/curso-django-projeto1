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
    username = forms.CharField(
        help_text=(
            "Username have letters, numbers or one of those @.+-_."
            " The length should be between 4 and 150 characters."
        ),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your username",
            }
        ),
        required=True,
        error_messages={
            "min_length": "Username must have at least 4 characters",
            "max_length": "Username must have less than 150 characters",
        },
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Lucas",
            }
        ),
        required=True,
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Pereira",
            }
        ),
        required=True,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your e-mail",
            }
        ),
        required=True,
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

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat your password",
                "class": "form-control",
            }
        ),
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

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        msg = "The entered passwords do not match. Please try again."

        if password != password2:
            raise ValidationError(
                {
                    "password": msg,
                    "password2": msg,
                }
            )
