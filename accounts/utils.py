import secrets
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    """Generate a 6-digit OTP"""
    return str(secrets.randbelow(900000) + 100000)


def send_otp_email(user, otp):
    """Send OTP verification email to user"""
    subject = "Verify Your Email - Kartavya Solar"
    message = f"""
Hi {user.first_name},

Welcome to Kartavya Solar!

Your email verification code is: {otp}

This code will expire in 10 minutes.

If you didn't create an account, please ignore this email.

Thanks,
Kartavya Solar Team
    """
    
    try:
        # Use explicit SMTP backend to ensure email is sent
        from django.core.mail import EmailMessage
        from django.core.mail.backends.smtp import EmailBackend
        
        # Create SMTP connection
        smtp_backend = EmailBackend(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            fail_silently=False,
        )
        
        # Create and send email
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            connection=smtp_backend,
        )
        email_message.send()
        
        print(f"✓ OTP email sent successfully to {user.email}")
        return True
    except Exception as e:
        print(f"✗ Error sending OTP email: {e}")
        import traceback
        traceback.print_exc()
        return False


def is_otp_valid(user):
    """Check if OTP is still valid (not expired)"""
    if not user.otp_created_at:
        return False
    
    expiry_time = user.otp_created_at + timedelta(minutes=10)
    return timezone.now() < expiry_time


def verify_otp(user, entered_otp):
    """Verify the OTP entered by user"""
    # Check if OTP exists
    if not user.otp_code:
        return False, "No OTP found. Please request a new one."
    
    # Check if OTP is expired
    if not is_otp_valid(user):
        return False, "OTP has expired. Please request a new one."
    
    # Check attempts
    if user.otp_attempts >= 3:
        return False, "Too many failed attempts. Please request a new OTP."
    
    # Verify OTP
    if user.otp_code == entered_otp:
        # Success - mark email as verified
        user.email_verified = True
        user.otp_code = None
        user.otp_created_at = None
        user.otp_attempts = 0
        user.save()
        return True, "Email verified successfully!"
    else:
        # Failed attempt
        user.otp_attempts += 1
        user.save()
        remaining = 3 - user.otp_attempts
        return False, f"Invalid OTP. {remaining} attempt(s) remaining."
