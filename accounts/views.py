from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SignupForm, LoginForm
from .utils import generate_otp, send_otp_email, verify_otp, is_otp_valid


def signup_view(request):
    # Get the next parameter from URL
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False  # Email not verified yet
            user.save()
            
            # Generate and send OTP
            otp = generate_otp()
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.otp_attempts = 0
            user.save()
            
            # Send OTP email
            if send_otp_email(user, otp):
                messages.success(request, f"Account created! Please check your email ({user.email}) for verification code.")
                # Store user ID in session for OTP verification
                request.session['verify_user_id'] = user.id
                request.session['verify_next'] = next_url
                return redirect("verify_otp")
            else:
                messages.error(request, "Account created but failed to send verification email. Please contact support.")
                return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    
    return render(request, "accounts/signup.html", {"form": form, "next": next_url})


def login_view(request):
    # Get the next parameter from URL
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if email is verified
            if not user.email_verified:
                messages.error(request, "Please verify your email before logging in. Check your inbox for the verification code.")
                request.session['verify_user_id'] = user.id
                return redirect("verify_otp")
            
            # Log the user in FIRST
            login(request, user)
            print(f"[DEBUG] User logged in: {user.email}")
            
            # Check if there's a pending cart addition
            pending_cart = request.session.get('pending_cart_add')
            print(f"[DEBUG] Pending cart data: {pending_cart}")
            
            if pending_cart:
                # Remove from session
                del request.session['pending_cart_add']
                print(f"[DEBUG] Found pending cart: {pending_cart}")
                
                # Process the pending cart addition
                from core.models import Product
                try:
                    product = Product.objects.get(id=pending_cart['product_id'], is_active=True)
                    quantity = pending_cart.get('quantity', product.min_order_quantity)
                    
                    # Import the helper function
                    from core.views import _process_add_to_cart
                    print(f"[DEBUG] Processing cart addition for product: {product.name}")
                    # This will redirect to cart page
                    return _process_add_to_cart(request, product, quantity)
                except Product.DoesNotExist:
                    messages.error(request, "Product not found.")
                    print(f"[DEBUG] Product not found: {pending_cart['product_id']}")
                    return redirect("home")
            
            # No pending cart - normal login flow
            messages.success(request, f"Welcome back, {user.first_name}!")
            print(f"[DEBUG] No pending cart, redirecting to: {next_url or 'home'}")
            
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()
    
    return render(request, "accounts/login.html", {"form": form, "next": next_url})


def verify_otp_view(request):
    """OTP verification page"""
    user_id = request.session.get('verify_user_id')
    if not user_id:
        messages.error(request, "No verification session found. Please sign up again.")
        return redirect("signup")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("signup")
    
    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()
        
        if not entered_otp:
            messages.error(request, "Please enter the OTP code.")
            return render(request, "accounts/verify_otp.html", {"user": user})
        
        # Verify OTP
        success, message = verify_otp(user, entered_otp)
        
        if success:
            messages.success(request, message)
            # Clear session
            del request.session['verify_user_id']
            next_url = request.session.pop('verify_next', None)
            
            # Log the user in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Check if there's a pending cart addition
            pending_cart = request.session.pop('pending_cart_add', None)
            if pending_cart:
                print(f"[DEBUG] Found pending cart after OTP: {pending_cart}")
                # Process the pending cart addition
                from core.models import Product
                try:
                    product = Product.objects.get(id=pending_cart['product_id'], is_active=True)
                    quantity = pending_cart.get('quantity', product.min_order_quantity)
                    
                    # Import the helper function
                    from core.views import _process_add_to_cart
                    print(f"[DEBUG] Processing cart addition after OTP for product: {product.name}")
                    return _process_add_to_cart(request, product, quantity)
                except Product.DoesNotExist:
                    messages.error(request, "Product not found.")
                    print(f"[DEBUG] Product not found after OTP: {pending_cart['product_id']}")
            
            # Only redirect to next URL if there was NO pending cart
            if next_url and not pending_cart:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, message)
    
    # Check if OTP is still valid
    otp_valid = is_otp_valid(user)
    
    return render(request, "accounts/verify_otp.html", {
        "user": user,
        "otp_valid": otp_valid,
        "attempts_left": 3 - user.otp_attempts
    })


def resend_otp_view(request):
    """Resend OTP to user"""
    user_id = request.session.get('verify_user_id')
    if not user_id:
        messages.error(request, "No verification session found.")
        return redirect("signup")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("signup")
    
    # Generate new OTP
    otp = generate_otp()
    user.otp_code = otp
    user.otp_created_at = timezone.now()
    user.otp_attempts = 0  # Reset attempts
    user.save()
    
    # Send OTP email
    if send_otp_email(user, otp):
        messages.success(request, f"New verification code sent to {user.email}")
    else:
        messages.error(request, "Failed to send verification email. Please try again.")
    
    return redirect("verify_otp")


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/?logout=success")
    return redirect("home")


from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view with console output"""
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.txt'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        """Override to show reset link clearly"""
        email = form.cleaned_data['email']
        
        # Get the user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset link
            reset_link = f"http://127.0.0.1:8000/accounts/password-reset-confirm/{uid}/{token}/"
            
            print("\n" + "=" * 80)
            print("PASSWORD RESET LINK GENERATED")
            print("=" * 80)
            print(f"Email: {email}")
            print(f"\nRESET LINK:")
            print(reset_link)
            print("\nCopy the link above and paste it in your browser!")
            print("=" * 80 + "\n")
            
        except User.DoesNotExist:
            print(f"\n[WARNING] No user found with email: {email}\n")
        
        # Still call parent to send email via console backend
        return super().form_valid(form)
