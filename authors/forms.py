from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    confirama_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'class': 'form-control',
            'label': 'Repeat your password',
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control input-register',
                'placeholder': 'Ex.: Lucas'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Pereira'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your e-mail'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your password'
            }),
        }
