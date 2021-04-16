from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)

from .models import UserBase


class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required", error_messages={"required": "An email is required"})

    class Meta:
        model = UserBase
        fields = (
            "username",
            "email",
        )


class RegistrationForm(forms.ModelForm):
    """
    Registration form
    """

    username = forms.CharField(label="Username", min_length=4, max_length=30, help_text="Required")
    email = forms.EmailField(max_length=100, help_text="Required", error_messages={"required": "An email is required"})
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ("username", "email",)


    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken, please use another email")

        return email

    def clean_password2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError("Password do not match")

        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control mb-3"})


class AccountLoginForm(AuthenticationForm):
    """
    Built-in AuthenticationFrom has 2 fields: username and password
    Override and add Bootstrap class to these 2 fields
    """

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Username", "id": "login-username"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )

    username = forms.CharField(
        label="Username",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Username",
                "id": "form-username",
                "readonly": "readonly",
            }
        ),
    )

    first_name = forms.CharField(
        label="First Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Firstname", "id": "form-firstname"}
        ),
    )

    class Meta:
        model = UserBase
        fields = (
            "email",
            "username",
            "first_name",
        )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Email", "id": "form-email"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = UserBase.objects.filter(email=email)
        if not user.exists():
            raise forms.ValidationError("We cannot find this email address")

        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-newpass"}
        ),
    )

    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-new-pass2"}
        ),
    )
