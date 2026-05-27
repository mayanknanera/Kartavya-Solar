from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .forms import SignupForm, LoginForm
from .utils import generate_otp, send_otp_email, verify_otp, is_otp_valid

User = get_user_model()


# ── Signup ────────────────────────────────────────────────────────────────────

def signup_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()

            otp = generate_otp()
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.otp_attempts = 0
            user.save()

            if send_otp_email(user, otp):
                messages.success(request, f"Account created! Check {user.email} for your verification code.")
                request.session["verify_user_id"] = user.id
                request.session["verify_next"] = next_url
                return redirect("verify_otp")
            else:
                messages.error(request, "Account created but we couldn't send the verification email. Please contact support.")
                return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form, "next": next_url})


# ── Login ─────────────────────────────────────────────────────────────────────

def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not user.email_verified:
                messages.error(request, "Please verify your email before logging in.")
                request.session["verify_user_id"] = user.id
                return redirect("verify_otp")

            login(request, user)

            # If the user had an item waiting to be added to cart, process it now
            pending_cart = request.session.pop("pending_cart_add", None)
            if pending_cart:
                from core.models import Product
                from core.views import _process_add_to_cart
                try:
                    product = Product.objects.get(id=pending_cart["product_id"], is_active=True)
                    quantity = pending_cart.get("quantity", product.min_order_quantity)
                    return _process_add_to_cart(request, product, quantity)
                except Product.DoesNotExist:
                    messages.error(request, "Product not found.")
                    return redirect("home")

            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect(next_url) if next_url else redirect("home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form, "next": next_url})


# ── OTP Verification ──────────────────────────────────────────────────────────

def verify_otp_view(request):
    user_id = request.session.get("verify_user_id")
    if not user_id:
        messages.error(request, "No verification session found. Please sign up again.")
        return redirect("signup")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("signup")

    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()

        if not entered_otp:
            messages.error(request, "Please enter the OTP code.")
            return render(request, "accounts/verify_otp.html", {"user": user})

        success, message = verify_otp(user, entered_otp)

        if success:
            messages.success(request, message)
            del request.session["verify_user_id"]
            next_url = request.session.pop("verify_next", None)

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            # Process any pending cart addition after OTP login
            pending_cart = request.session.pop("pending_cart_add", None)
            if pending_cart:
                from core.models import Product
                from core.views import _process_add_to_cart
                try:
                    product = Product.objects.get(id=pending_cart["product_id"], is_active=True)
                    quantity = pending_cart.get("quantity", product.min_order_quantity)
                    return _process_add_to_cart(request, product, quantity)
                except Product.DoesNotExist:
                    messages.error(request, "Product not found.")

            return redirect(next_url) if next_url else redirect("home")
        else:
            messages.error(request, message)

    return render(request, "accounts/verify_otp.html", {
        "user": user,
        "otp_valid": is_otp_valid(user),
        "attempts_left": 3 - user.otp_attempts,
    })


def resend_otp_view(request):
    user_id = request.session.get("verify_user_id")
    if not user_id:
        messages.error(request, "No verification session found.")
        return redirect("signup")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("signup")

    otp = generate_otp()
    user.otp_code = otp
    user.otp_created_at = timezone.now()
    user.otp_attempts = 0
    user.save()

    if send_otp_email(user, otp):
        messages.success(request, f"New verification code sent to {user.email}")
    else:
        messages.error(request, "Failed to send verification email. Please try again.")

    return redirect("verify_otp")


# ── Logout ────────────────────────────────────────────────────────────────────

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/?logout=success")
    return redirect("home")


# ── Password Reset ────────────────────────────────────────────────────────────

class CustomPasswordResetView(PasswordResetView):
    """Standard password reset — also prints the reset link to the console for easy dev testing."""

    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.txt"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://127.0.0.1:8000/accounts/password-reset-confirm/{uid}/{token}/"
            print(f"\n{'='*60}\nPASSWORD RESET LINK\nEmail: {email}\n{reset_link}\n{'='*60}\n")
        except User.DoesNotExist:
            pass  # Don't reveal whether the email exists

        return super().form_valid(form)
