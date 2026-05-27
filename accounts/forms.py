import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# Shared CSS class for all form inputs
INPUT_CLASS = (
    "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 "
    "focus:outline-none focus:border-orange-500 focus:ring-2 "
    "focus:ring-orange-500/20 transition-all"
)


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "John", "minlength": "2"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Doe"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "john@example.com"}),
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": INPUT_CLASS,
            "placeholder": "9876543210",
            "pattern": "[6-9][0-9]{9}",
            "maxlength": "10",
            "title": "Enter a valid 10-digit mobile number starting with 6-9",
        }),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "••••••••"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "••••••••"}),
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone", "password1", "password2")

    def clean_first_name(self):
        name = self.cleaned_data.get("first_name", "").strip()
        if len(name) < 2:
            raise ValidationError("First name must be at least 2 characters.")
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get("last_name", "").strip()
        if name and len(name) < 2:
            raise ValidationError("Last name must be at least 2 characters.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        phone = re.sub(r"[\s\-\(\)]", "", phone)

        # Strip country code if present
        if phone.startswith("+91"):
            phone = phone[3:]
        elif phone.startswith("91") and len(phone) == 12:
            phone = phone[2:]

        if not phone.isdigit():
            raise ValidationError("Phone number should contain only digits.")
        if len(phone) != 10:
            raise ValidationError("Phone number must be 10 digits.")
        if phone[0] not in "6789":
            raise ValidationError("Enter a valid 10-digit mobile number starting with 6-9.")

        return phone


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "your@email.com"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "••••••••"}),
    )
