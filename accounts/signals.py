from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib import messages


@receiver(pre_social_login)
def set_email_verified_for_social_login(sender, request, sociallogin, **kwargs):
    """
    Automatically verify email for users logging in via social accounts (Google, etc.)
    since these providers already verify email addresses.
    """
    if sociallogin.is_existing:
        # Existing user - ensure email is verified
        user = sociallogin.user
        if not user.email_verified:
            user.email_verified = True
            user.save()
    else:
        # New user - will be set after user is created
        # We'll handle this in the post_social_login signal
        pass


@receiver(pre_social_login)
def verify_new_social_user(sender, request, sociallogin, **kwargs):
    """
    Set email_verified=True for new users signing up via social accounts.
    """
    if not sociallogin.is_existing:
        # This is a new user signing up via social account
        # Set email_verified in the user data before saving
        user = sociallogin.user
        user.email_verified = True


@receiver(pre_social_login)
def handle_pending_cart_before_oauth(sender, request, sociallogin, **kwargs):
    """
    Check for pending cart BEFORE OAuth completes and set redirect flag.
    This fires before get_login_redirect_url is called.
    """
    pending_cart = request.session.get('pending_cart_add')
    if pending_cart:
        print(f"[DEBUG] pre_social_login: Found pending cart: {pending_cart}")
        # Set redirect flag BEFORE adapter is called
        request.session['redirect_to_cart'] = True
        request.session.modified = True
        print(f"[DEBUG] pre_social_login: Set redirect flag to True")


# Handle pending cart additions after social login
from allauth.account.signals import user_logged_in

@receiver(user_logged_in)
def process_pending_cart_after_social_login(sender, request, user, **kwargs):
    """
    Process pending cart additions after successful social login (Google OAuth).
    This adds the product to cart after login is complete.
    """
    pending_cart = request.session.pop('pending_cart_add', None)
    if pending_cart:
        print(f"[DEBUG] user_logged_in: Found pending cart: {pending_cart}")
        from core.models import Product, Cart, CartItem
        
        try:
            product = Product.objects.get(id=pending_cart['product_id'], is_active=True)
            quantity = pending_cart.get('quantity', product.min_order_quantity)
            
            # Add to cart
            cart, _ = Cart.objects.get_or_create(user=user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            
            cart_item.save()
            messages.success(request, f"Added {product.name} to your cart!")
            print(f"[DEBUG] user_logged_in: Product added to cart successfully")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            print(f"[DEBUG] user_logged_in: Product not found: {pending_cart['product_id']}")




