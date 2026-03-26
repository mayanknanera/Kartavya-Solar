from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import re


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "John",
                "minlength": "2",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "Doe",
                "minlength": "2",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "john@example.com",
            }
        )
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "9876543210",
                "pattern": "[6-9][0-9]{9}",
                "maxlength": "10",
                "title": "Please enter a valid 10-digit mobile number starting with 6-9",
            }
        ),
        required=True,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "••••••••",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "••••••••",
            }
        ),
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()
        if not first_name:
            raise ValidationError("First name is required.")
        if len(first_name) < 2:
            raise ValidationError("First name must be at least 2 characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()
        # Last name is optional, but if provided, must be at least 2 characters
        if last_name and len(last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters.")
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            phone = phone.strip()
            phone = re.sub(r"[\s\-\(\)]", "", phone)

            if phone.startswith("+91"):
                phone = phone[3:]
            elif phone.startswith("91") and len(phone) == 12:
                phone = phone[2:]

            if not phone.isdigit():
                raise ValidationError("Phone number should contain only digits.")

            if len(phone) != 10:
                raise ValidationError("Phone number must be 10 digits.")
            
            # Validate Indian mobile number pattern (starts with 6-9)
            if not phone[0] in ['6', '7', '8', '9']:
                raise ValidationError("Please enter a valid 10-digit mobile number starting with 6-9.")

        return phone

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "your@email.com",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all",
                "placeholder": "••••••••",
            }
        )
    )
