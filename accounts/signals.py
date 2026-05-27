from django.dispatch import receiver
from django.contrib import messages
from allauth.socialaccount.signals import pre_social_login
from allauth.account.signals import user_logged_in


@receiver(pre_social_login)
def mark_social_user_email_verified(sender, request, sociallogin, **kwargs):
    """
    Google already verifies email addresses, so we mark the user's email
    as verified automatically when they log in via Google.
    """
    user = sociallogin.user
    if not user.email_verified:
        user.email_verified = True
        if sociallogin.is_existing:
            user.save()


@receiver(pre_social_login)
def set_cart_redirect_flag(sender, request, sociallogin, **kwargs):
    """
    If the user had a pending cart addition before starting OAuth,
    set a flag so the adapter redirects them to the cart after login.
    """
    if request.session.get("pending_cart_add"):
        request.session["redirect_to_cart"] = True
        request.session.modified = True


@receiver(user_logged_in)
def process_pending_cart_after_social_login(sender, request, user, **kwargs):
    """
    After a successful social login, add any pending cart item to the user's cart.
    """
    pending_cart = request.session.pop("pending_cart_add", None)
    if not pending_cart:
        return

    from core.models import Product, Cart, CartItem

    try:
        product = Product.objects.get(id=pending_cart["product_id"], is_active=True)
        quantity = pending_cart.get("quantity", product.min_order_quantity)

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()
        messages.success(request, f"Added {product.name} to your cart!")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
