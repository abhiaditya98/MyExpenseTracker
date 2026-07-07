from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message="Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
    )


    UserName = forms.CharField(
        max_length=150,
        required=True,
        label = "User Name",
        validators = [username_validator],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username"}
        ),
    )

    Email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password", "id": "password-field"}
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm your password"}
        ),
    )

    class Meta:
        model = User
        fields = ["UserName", "Email", "password1", "password2"]


