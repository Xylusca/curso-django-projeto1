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

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Lucas",
            }
        ),
        error_messages={
            "required": "Write your first name",
        },
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Pereira",
            }
        ),
        error_messages={
            "required": "Write your last name",
        },
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your e-mail",
            }
        ),
        help_text="The e-mail must be valid.",
        error_messages={"required": "E-mail is required"},
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
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your username"}
            ),
        }

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
