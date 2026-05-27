"""
Tests for the accounts app.
Covers: CustomUser model, SignupForm, LoginForm, OTP utils, and all auth views.
"""
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from accounts.forms import SignupForm, LoginForm
from accounts.utils import generate_otp, is_otp_valid, verify_otp

User = get_user_model()


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_user(email="test@example.com", password="StrongPass123", verified=True, **kwargs):
    """Create a verified user ready for login."""
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=kwargs.get("first_name", "Test"),
        **{k: v for k, v in kwargs.items() if k != "first_name"},
    )
    user.email_verified = verified
    user.save()
    return user


# ══════════════════════════════════════════════════════════════════════════════
# MODEL TESTS
# ══════════════════════════════════════════════════════════════════════════════

class CustomUserModelTest(TestCase):

    def test_create_user_uses_email_as_username(self):
        user = User.objects.create_user(email="a@b.com", password="pass", first_name="A")
        self.assertEqual(user.email, "a@b.com")
        self.assertIsNone(user.username)

    def test_email_is_unique(self):
        User.objects.create_user(email="dup@b.com", password="pass", first_name="A")
        with self.assertRaises(Exception):
            User.objects.create_user(email="dup@b.com", password="pass", first_name="B")

    def test_str_returns_email(self):
        user = User.objects.create_user(email="str@b.com", password="pass", first_name="S")
        self.assertEqual(str(user), "str@b.com")

    def test_email_verified_defaults_false(self):
        user = User.objects.create_user(email="v@b.com", password="pass", first_name="V")
        self.assertFalse(user.email_verified)

    def test_superuser_email_verified_true(self):
        admin = User.objects.create_superuser(email="admin@b.com", password="pass")
        self.assertTrue(admin.email_verified)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="pass", first_name="X")

    def test_otp_fields_default_null(self):
        user = User.objects.create_user(email="otp@b.com", password="pass", first_name="O")
        self.assertIsNone(user.otp_code)
        self.assertIsNone(user.otp_created_at)
        self.assertEqual(user.otp_attempts, 0)


# ══════════════════════════════════════════════════════════════════════════════
# OTP UTILITY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class OTPUtilsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="otp@test.com", password="pass", first_name="OTP")

    def test_generate_otp_is_6_digits(self):
        otp = generate_otp()
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    def test_generate_otp_is_random(self):
        otps = {generate_otp() for _ in range(20)}
        self.assertGreater(len(otps), 1)

    def test_is_otp_valid_true_when_fresh(self):
        self.user.otp_created_at = timezone.now()
        self.assertTrue(is_otp_valid(self.user))

    def test_is_otp_valid_false_when_expired(self):
        self.user.otp_created_at = timezone.now() - timedelta(minutes=11)
        self.assertFalse(is_otp_valid(self.user))

    def test_is_otp_valid_false_when_no_timestamp(self):
        self.user.otp_created_at = None
        self.assertFalse(is_otp_valid(self.user))

    def test_verify_otp_success(self):
        self.user.otp_code = "123456"
        self.user.otp_created_at = timezone.now()
        self.user.otp_attempts = 0
        self.user.save()

        success, msg = verify_otp(self.user, "123456")
        self.assertTrue(success)
        self.assertIn("verified", msg.lower())
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)
        self.assertIsNone(self.user.otp_code)

    def test_verify_otp_wrong_code_increments_attempts(self):
        self.user.otp_code = "123456"
        self.user.otp_created_at = timezone.now()
        self.user.otp_attempts = 0
        self.user.save()

        success, msg = verify_otp(self.user, "000000")
        self.assertFalse(success)
        self.user.refresh_from_db()
        self.assertEqual(self.user.otp_attempts, 1)

    def test_verify_otp_expired(self):
        self.user.otp_code = "123456"
        self.user.otp_created_at = timezone.now() - timedelta(minutes=15)
        self.user.otp_attempts = 0
        self.user.save()

        success, msg = verify_otp(self.user, "123456")
        self.assertFalse(success)
        self.assertIn("expired", msg.lower())

    def test_verify_otp_too_many_attempts(self):
        self.user.otp_code = "123456"
        self.user.otp_created_at = timezone.now()
        self.user.otp_attempts = 3
        self.user.save()

        success, msg = verify_otp(self.user, "123456")
        self.assertFalse(success)
        self.assertIn("attempts", msg.lower())

    def test_verify_otp_no_code(self):
        self.user.otp_code = None
        self.user.save()

        success, msg = verify_otp(self.user, "123456")
        self.assertFalse(success)


# ══════════════════════════════════════════════════════════════════════════════
# FORM TESTS
# ══════════════════════════════════════════════════════════════════════════════

class SignupFormTest(TestCase):

    def _valid_data(self, **overrides):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        data.update(overrides)
        return data

    def test_valid_form(self):
        form = SignupForm(data=self._valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_short_first_name_invalid(self):
        form = SignupForm(data=self._valid_data(first_name="A"))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_short_last_name_invalid(self):
        form = SignupForm(data=self._valid_data(last_name="X"))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_empty_last_name_valid(self):
        form = SignupForm(data=self._valid_data(last_name=""))
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_phone_letters(self):
        form = SignupForm(data=self._valid_data(phone="abcdefghij"))
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_invalid_phone_starts_with_5(self):
        form = SignupForm(data=self._valid_data(phone="5123456789"))
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_invalid_phone_too_short(self):
        form = SignupForm(data=self._valid_data(phone="98765"))
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_phone_with_country_code_stripped(self):
        form = SignupForm(data=self._valid_data(phone="+919876543210"))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["phone"], "9876543210")

    def test_duplicate_email_invalid(self):
        User.objects.create_user(email="john@example.com", password="pass", first_name="J")
        form = SignupForm(data=self._valid_data())
        self.assertFalse(form.is_valid())

    def test_password_mismatch_invalid(self):
        form = SignupForm(data=self._valid_data(password2="DifferentPass123!"))
        self.assertFalse(form.is_valid())


# ══════════════════════════════════════════════════════════════════════════════
# VIEW TESTS — AUTH
# ══════════════════════════════════════════════════════════════════════════════

class SignupViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("signup")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch("accounts.views.send_otp_email", return_value=True)
    def test_valid_post_creates_user_and_redirects(self, mock_email):
        response = self.client.post(self.url, {
            "first_name": "Jane",
            "email": "jane@example.com",
            "phone": "9876543210",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertRedirects(response, reverse("verify_otp"))
        self.assertTrue(User.objects.filter(email="jane@example.com").exists())

    @patch("accounts.views.send_otp_email", return_value=True)
    def test_new_user_email_not_verified_yet(self, mock_email):
        self.client.post(self.url, {
            "first_name": "Jane",
            "email": "jane2@example.com",
            "phone": "9876543210",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        user = User.objects.get(email="jane2@example.com")
        self.assertFalse(user.email_verified)

    def test_invalid_post_stays_on_page(self):
        response = self.client.post(self.url, {"email": "bad"})
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("login")
        self.user = make_user(email="login@test.com", password="StrongPass123")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_login_redirects_home(self):
        response = self.client.post(self.url, {
            "username": "login@test.com",
            "password": "StrongPass123",
        })
        self.assertRedirects(response, reverse("home"))

    def test_wrong_password_stays_on_page(self):
        response = self.client.post(self.url, {
            "username": "login@test.com",
            "password": "WrongPassword",
        })
        self.assertEqual(response.status_code, 200)

    def test_unverified_user_redirected_to_otp(self):
        unverified = make_user(email="unverified@test.com", password="StrongPass123", verified=False)
        response = self.client.post(self.url, {
            "username": "unverified@test.com",
            "password": "StrongPass123",
        })
        self.assertRedirects(response, reverse("verify_otp"))

    def test_login_with_next_param_redirects_correctly(self):
        response = self.client.post(
            self.url + "?next=/products/",
            {"username": "login@test.com", "password": "StrongPass123"},
        )
        self.assertRedirects(response, "/products/")


class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.client.force_login(self.user)

    def test_post_logs_out_and_redirects(self):
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, "/?logout=success")

    def test_get_redirects_home_without_logout(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))


class OTPViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="otp@view.com", password="pass", first_name="OTP"
        )
        self.user.otp_code = "123456"
        self.user.otp_created_at = timezone.now()
        self.user.otp_attempts = 0
        self.user.save()
        session = self.client.session
        session["verify_user_id"] = self.user.id
        session.save()

    def test_get_verify_otp_page(self):
        response = self.client.get(reverse("verify_otp"))
        self.assertEqual(response.status_code, 200)

    def test_correct_otp_logs_in_and_redirects(self):
        response = self.client.post(reverse("verify_otp"), {"otp": "123456"})
        self.assertRedirects(response, reverse("home"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)

    def test_wrong_otp_stays_on_page(self):
        response = self.client.post(reverse("verify_otp"), {"otp": "000000"})
        self.assertEqual(response.status_code, 200)

    def test_no_session_redirects_to_signup(self):
        self.client.session.flush()
        response = self.client.get(reverse("verify_otp"))
        self.assertRedirects(response, reverse("signup"))
