import re
import traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import models, transaction
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.conf import settings

from .models import Product, Cart, CartItem, Order, OrderItem


# ── Helpers ───────────────────────────────────────────────────────────────────

def _safe_int(value, default):
    """Convert value to int, returning default on failure."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _cart_total_quantity(cart):
    """Return the total number of items across all cart lines."""
    if not cart:
        return 0
    return sum(item.quantity for item in cart.items.all())


# ── Static Pages ──────────────────────────────────────────────────────────────

def home_view(request):
    if request.GET.get("logout") == "success":
        messages.success(request, "You have been logged out successfully.")
    return render(request, "home.html")


def about_view(request):
    return render(request, "about.html")


# ── Contact ───────────────────────────────────────────────────────────────────

@login_required
def contact_view(request):
    initial_data = {
        "name": f"{request.user.first_name} {request.user.last_name}".strip() or request.user.email.split("@")[0],
        "email": request.user.email,
        "phone": request.user.phone,
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        service = request.POST.get("service", "").strip()
        message_text = request.POST.get("message", "").strip()

        errors = []

        if not all([name, phone, email, service]):
            errors.append("Please fill in all required fields.")
        if name and len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        if phone and not re.match(r"^[6-9]\d{9}$", phone):
            errors.append("Enter a valid 10-digit mobile number starting with 6-9.")
        if email:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Enter a valid email address.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "contact.html", {"initial_data": initial_data})

        subject = f"New Contact Form Submission - {service}"
        body = (
            f"New Contact Form Submission from Kartavya Solar Website\n\n"
            f"Name: {name}\nPhone: {phone}\nEmail: {email}\n"
            f"Service: {service}\n\nMessage:\n{message_text or 'No message provided'}"
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
                to=[settings.EMAIL_HOST_USER],
                connection=smtp,
            ).send()
            messages.success(request, "Thank you! We'll get back to you within 24 hours.")
            return redirect("contact")
        except Exception as e:
            print(f"Contact email error: {e}")
            traceback.print_exc()
            messages.error(request, "Sorry, there was an error sending your message. Please try again.")
            return render(request, "contact.html", {"initial_data": initial_data})

    return render(request, "contact.html", {"initial_data": initial_data})


# ── Profile ───────────────────────────────────────────────────────────────────

@login_required
def profile_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    active_tab = "profile"

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            city = request.POST.get("city", "").strip()
            state = request.POST.get("state", "").strip()
            pincode = request.POST.get("pincode", "").strip()

            errors = []
            if not first_name or len(first_name) < 2:
                errors.append("First name must be at least 2 characters.")
            if last_name and len(last_name) < 2:
                errors.append("Last name must be at least 2 characters.")
            if phone and not re.match(r"^[6-9]\d{9}$", phone):
                errors.append("Enter a valid 10-digit mobile number starting with 6-9.")
            if pincode and (not pincode.isdigit() or len(pincode) != 6):
                errors.append("Enter a valid 6-digit pincode.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, "profile.html", {"active_tab": active_tab, "next": next_url})

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.phone = phone
            request.user.address = address
            request.user.city = city
            request.user.state = state
            request.user.pincode = pincode
            request.user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect(next_url) if next_url else redirect("profile")

        elif action == "change_password":
            active_tab = "password"
            current_password = request.POST.get("current_password", "")
            new_password = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")

            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
            elif len(new_password) < 8:
                messages.error(request, "New password must be at least 8 characters.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")
                return redirect("profile")

            return render(request, "profile.html", {"active_tab": active_tab, "next": next_url})

    return render(request, "profile.html", {"active_tab": active_tab, "next": next_url})


# ── Products ──────────────────────────────────────────────────────────────────

def product_list(request):
    products = Product.objects.filter(is_active=True)

    category_filter = request.GET.get("category", "")
    search_query = request.GET.get("search", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    stock_filter = request.GET.get("stock", "")
    sort_by = request.GET.get("sort", "")

    if category_filter:
        products = products.filter(category=category_filter)
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query)
        )
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if stock_filter == "in_stock":
        products = products.filter(stock_quantity__gt=0)
    elif stock_filter == "out_of_stock":
        products = products.filter(stock_quantity=0)

    sort_map = {"price_low": "price", "price_high": "-price", "name": "name"}
    products = products.order_by(sort_map.get(sort_by, "-id"))

    return render(request, "products/product_list.html", {
        "products": products,
        "search_query": search_query,
        "min_price": min_price,
        "max_price": max_price,
        "stock_filter": stock_filter,
        "category_filter": category_filter,
        "categories": Product.CATEGORY_CHOICES,
        "sort_by": sort_by,
        "total_count": products.count(),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "products/product_detail.html", {"product": product})


# ── Cart ──────────────────────────────────────────────────────────────────────

@require_POST
def add_to_cart(request, product_id):
    """
    Add a product to the cart.
    If the user is not logged in, save the intent in the session and redirect to login.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = _safe_int(request.POST.get("quantity", product.min_order_quantity), product.min_order_quantity)

    if not request.user.is_authenticated:
        request.session["pending_cart_add"] = {
            "product_id": product_id,
            "quantity": quantity,
            "product_slug": product.slug,
        }
        request.session.modified = True
        messages.info(request, "Please login to add items to your cart.")
        return redirect(reverse("login"))

    return _process_add_to_cart(request, product, quantity)


def _process_add_to_cart(request, product, quantity):
    """Internal helper: validate and add a product to the authenticated user's cart."""
    if product.stock_quantity < quantity:
        messages.error(request, f"Only {product.stock_quantity} units left for {product.name}.")
        return redirect("product_detail", slug=product.slug)

    if quantity < product.min_order_quantity:
        messages.warning(request, f"Minimum order quantity for {product.name} is {product.min_order_quantity}.")
        return redirect("product_detail", slug=product.slug)

    if product.max_order_quantity and quantity > product.max_order_quantity:
        messages.warning(request, f"Maximum order quantity for {product.name} is {product.max_order_quantity}.")
        return redirect("product_detail", slug=product.slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        new_quantity = cart_item.quantity + quantity
        if product.stock_quantity < new_quantity:
            messages.error(request, f"Cannot add more. You have {cart_item.quantity} in cart and only {product.stock_quantity} available.")
            return redirect("cart")
        cart_item.quantity = new_quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, f"Added {product.name} to your cart!")
    return redirect("cart")


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.all() if cart else []
    total = sum(item.get_total_price() for item in items)
    return render(request, "cart/cart.html", {"cart": cart, "items": items, "total": total})


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update the quantity of a cart item (AJAX-friendly)."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product = cart_item.product
    quantity = _safe_int(request.POST.get("quantity"), cart_item.quantity)

    success = False
    message = ""

    if quantity > 0:
        if quantity < product.min_order_quantity:
            message = f"Minimum order quantity is {product.min_order_quantity}."
        elif product.max_order_quantity and quantity > product.max_order_quantity:
            message = f"Maximum order quantity is {product.max_order_quantity}."
        elif product.stock_quantity < quantity:
            message = f"Only {product.stock_quantity} units available."
        else:
            cart_item.quantity = quantity
            cart_item.save()
            success = True
            message = "Cart updated."
    else:
        cart_item.delete()
        success = True
        cart = Cart.objects.filter(user=request.user).first()
        message = "Cart is now empty." if not (cart and cart.items.exists()) else "Item removed."

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        from django.http import JsonResponse
        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.all() if cart else []
        total = sum(item.get_total_price() for item in items)
        return JsonResponse({
            "success": success,
            "message": message,
            "item_id": item_id,
            "quantity": cart_item.quantity if (quantity > 0 and success) else 0,
            "item_total": float(cart_item.get_total_price()) if (quantity > 0 and success) else 0,
            "cart_total": float(total),
            "cart_count": _cart_total_quantity(cart),
        })

    if success:
        messages.success(request, message)
    else:
        messages.warning(request, message)
    return redirect("cart")


@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Remove an item from the cart (AJAX-friendly)."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart = cart_item.cart
    cart_item.delete()

    items = cart.items.all()
    is_empty = not items.exists()
    message = "Cart is now empty." if is_empty else f"{product_name} removed from cart."

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        from django.http import JsonResponse
        total = sum(item.get_total_price() for item in items)
        return JsonResponse({
            "success": True,
            "message": message,
            "cart_total": float(total),
            "cart_count": _cart_total_quantity(cart),
            "cart_empty": is_empty,
        })

    if is_empty:
        messages.info(request, message)
    else:
        messages.success(request, message)
    return redirect("cart")


@login_required
@require_POST
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart and cart.items.exists():
        cart.items.all().delete()
        messages.success(request, "Cart cleared.")
    else:
        messages.info(request, "Your cart is already empty.")
    return redirect("cart")


# ── Checkout & Orders ─────────────────────────────────────────────────────────

@login_required
@transaction.atomic
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("product_list")

    if request.method == "POST":
        # Final stock check
        for item in cart.items.all():
            if item.product.stock_quantity < item.quantity:
                messages.error(request, f"{item.product.name} has insufficient stock. Please adjust your cart.")
                return redirect("cart")

        order = Order.objects.create(user=request.user, payment_method="COD", status="PLACED")

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            item.product.stock_quantity -= item.quantity
            item.product.save()

        cart.items.all().delete()
        messages.success(request, "Order placed successfully! Payment is Cash on Delivery.")
        return redirect("order_success")

    total = sum(item.get_total_price() for item in cart.items.all())
    return render(request, "checkout/checkout.html", {"cart": cart, "total": total})


@login_required
def order_success(request):
    return render(request, "orders/order_success.html")


@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    for order in orders:
        order.total = sum(item.price * item.quantity for item in order.items.all())
    return render(request, "orders/orders.html", {"orders": orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    subtotal = sum(item.price * item.quantity for item in items)
    return render(request, "orders/order_detail.html", {"order": order, "items": items, "subtotal": subtotal})


@login_required
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ("COMPLETED", "CANCELLED"):
        messages.error(request, f"Cannot cancel — order is already {order.status.lower()}.")
        return redirect("order_detail", order_id=order_id)

    for item in order.items.all():
        item.product.stock_quantity += item.quantity
        item.product.save()

    order.status = "CANCELLED"
    order.save()

    messages.success(request, f"Order #{order.id} cancelled. Stock has been restored.")
    return redirect("order_detail", order_id=order_id)
