import secrets
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


def generate_otp():
    """Return a random 6-digit OTP string."""
    return str(secrets.randbelow(900000) + 100000)


def send_otp_email(user, otp):
    """Send the OTP verification email. Returns True on success, False on failure."""
    subject = "Verify Your Email - Kartavya Solar"
    body = (
        f"Hi {user.first_name},\n\n"
        f"Welcome to Kartavya Solar!\n\n"
        f"Your email verification code is: {otp}\n\n"
        f"This code expires in 10 minutes.\n\n"
        f"If you didn't create an account, please ignore this email.\n\n"
        f"Thanks,\nKartavya Solar Team"
    )

    try:
        smtp = EmailBackend(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            fail_silently=False,
        )
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            connection=smtp,
        ).send()
        return True
    except Exception as e:
        print(f"OTP email error: {e}")
        return False


def is_otp_valid(user):
    """Return True if the user's OTP has not expired (10-minute window)."""
    if not user.otp_created_at:
        return False
    return timezone.now() < user.otp_created_at + timedelta(minutes=10)


def verify_otp(user, entered_otp):
    """
    Verify the OTP entered by the user.
    Returns (success: bool, message: str).
    """
    if not user.otp_code:
        return False, "No OTP found. Please request a new one."

    if not is_otp_valid(user):
        return False, "OTP has expired. Please request a new one."

    if user.otp_attempts >= 3:
        return False, "Too many failed attempts. Please request a new OTP."

    if user.otp_code == entered_otp:
        user.email_verified = True
        user.otp_code = None
        user.otp_created_at = None
        user.otp_attempts = 0
        user.save()
        return True, "Email verified successfully!"

    user.otp_attempts += 1
    user.save()
    remaining = 3 - user.otp_attempts
    return False, f"Invalid OTP. {remaining} attempt(s) remaining."
