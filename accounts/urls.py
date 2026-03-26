from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Regular auth URLs
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # OTP verification URLs
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("resend-otp/", views.resend_otp_view, name="resend_otp"),
    # ========== PASSWORD RESET FLOW ==========
    # STEP 1: User enters email to reset password
    path(
        "password-reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    # STEP 2: Confirmation page (email sent successfully)
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"  # "Check your email" page
        ),
        name="password_reset_done",
    ),
    # STEP 3: User clicks link from email (has unique ID and token)
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",  # Form to enter new password
            success_url="/accounts/password-reset-complete/",  # Where to go after setting new password
        ),
        name="password_reset_confirm",
    ),
    # STEP 4: Success page (password reset complete)
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"  # "Password reset successful" page
        ),
        name="password_reset_complete",
    ),
]
